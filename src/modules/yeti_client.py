import os
import httpx
from src.config import settings
from src.logger import logger, get_search_logger
from src.utils.xml_parser import unescape_xml, parse_yeti_xml_response

class YetiClient:
    def __init__(self):
        self.url = settings.YETI_API_URL
        self.agency_code = settings.YETI_AGENCY_CODE
        self.password = settings.YETI_PASSWORD
        self.headers = {'Content-Type': 'text/xml'}
        self.session_store = {}
        self.sequence_store = {}

    def _format_date(self, date_str: str) -> str:
        """Helper to format date for Yeti API (YYYYMMDD). Returns empty string if invalid/none."""
        if not date_str or date_str.lower() == 'string':
            return ""
        # Remove hyphens if present (e.g., 2026-02-20 -> 20260220)
        return date_str.replace('-', '')

    def log_to_file(self, search_id: str, filename: str, content: str):
        # Ensure directory exists (though logger usually does this)
        log_dir = f"logs/{search_id}"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        # Get and increment sequence number for this search_id
        seq_num = self.sequence_store.get(search_id, 1)
        self.sequence_store[search_id] = seq_num + 1
        
        # Prefix filename with sequence number
        full_filename = f"{seq_num:02d}_{filename}"
            
        file_path = os.path.join(log_dir, full_filename)
        # Unescape XML for readability
        try:
            readable_content = unescape_xml(content)
        except Exception:
            readable_content = content
            
        with open(file_path, "w") as f:
            f.write(readable_content)

    async def get_flight_availability(self, request_data, search_id: str):
        search_logger = get_search_logger(search_id)
        
        payload = f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
      <tem:FlightAvailability>
         <tem:strAgencyCode>{self.agency_code}</tem:strAgencyCode>
         <tem:strPassword>{self.password}</tem:strPassword>
         <tem:strOrigin>{request_data.origin}</tem:strOrigin>
         <tem:strDestination>{request_data.destination}</tem:strDestination>
         <tem:strDepartFrom>{self._format_date(request_data.depart_date)}</tem:strDepartFrom>
         <tem:strDepartTo>{self._format_date(request_data.depart_date)}</tem:strDepartTo>
         <tem:strReturnFrom>{self._format_date(request_data.return_date)}</tem:strReturnFrom>
         <tem:strReturnTo>{self._format_date(request_data.return_date)}</tem:strReturnTo>
         <tem:iAdult>{request_data.adults}</tem:iAdult>
         <tem:iChild>{request_data.children}</tem:iChild>
         <tem:iInfant>{request_data.infants}</tem:iInfant>
         <tem:iOther>{request_data.others}</tem:iOther>
         <tem:nationality>{request_data.nationality}</tem:nationality>
         <tem:strBookingClass></tem:strBookingClass>
         <tem:strBoardingClass></tem:strBoardingClass>
         <tem:strPromoCode></tem:strPromoCode>
         <tem:strLanguageCode>EN</tem:strLanguageCode>
      </tem:FlightAvailability>
   </soapenv:Body>
</soapenv:Envelope>"""
        
        # Load cookies if exist (though availability usually doesn't need prev session, but good for consistency)
        cookies = self.session_store.get(search_id)

        async with httpx.AsyncClient(cookies=cookies) as client:
            try:
                search_logger.info(f"Sending FlightAvailability request to {self.url} for origin={request_data.origin} destination={request_data.destination} date={request_data.depart_date}")
                self.log_to_file(search_id, "FlightAvailability_RQ.xml", payload)
                
                response = await client.post(self.url, headers=self.headers, content=payload, timeout=30.0)
                response.raise_for_status()
                
                # Update cookies
                if response.cookies:
                    self.session_store[search_id] = response.cookies

                search_logger.info(f"Received response from Yeti API: status={response.status_code}")
                self.log_to_file(search_id, "FlightAvailability_RS.xml", response.text)
                return response.text
            except httpx.HTTPError as e:
                search_logger.error(f"Yeti API error: {e}")
                raise Exception(f"Yeti API error: {e}")

    async def service_initialize(self, search_id: str):
        search_logger = get_search_logger(search_id)
        
        payload = f"""<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:tem="http://tempuri.org/">
   <soap:Header/>
   <soap:Body>
      <tem:ServiceInitialize>
         <tem:strAgencyCode>{self.agency_code}</tem:strAgencyCode>
         <tem:strUserName>{settings.YETI_USERNAME}</tem:strUserName>
         <tem:strPassword>{self.password}</tem:strPassword>
         <tem:strLanguageCode>EN</tem:strLanguageCode>
      </tem:ServiceInitialize>
   </soap:Body>
</soap:Envelope>"""
        
        # New session logic could be enforced here by ignoring previous cookies, but let's be safe
        cookies = self.session_store.get(search_id)
        
        async with httpx.AsyncClient(cookies=cookies) as client:
            try:
                search_logger.info(f"Sending ServiceInitialize request to {self.url}")
                self.log_to_file(search_id, "ServiceInitialize_RQ.xml", payload)
                
                response = await client.post(self.url, headers=self.headers, content=payload, timeout=30.0)
                response.raise_for_status()
                
                # IMPORTANT: Save the session cookies
                if response.cookies:
                    self.session_store[search_id] = response.cookies
                    search_logger.info(f"Session cookies saved for search_id={search_id}")

                search_logger.info(f"Received response from Yeti API ServiceInitialize: status={response.status_code}")
                self.log_to_file(search_id, "ServiceInitialize_RS.xml", response.text)
                return response.text
            except httpx.HTTPError as e:
                search_logger.error(f"Yeti API error in ServiceInitialize: {e}")
                raise Exception(f"Yeti API error in ServiceInitialize: {e}")

    async def flight_add(self, request_data, search_id: str):
        search_logger = get_search_logger(search_id)
        
        inner_xml = f"""<Booking>
        	<Header>
        		<adult>{request_data.adults}</adult>
        		<child>{request_data.children}</child>
        		<infant>{request_data.infants}</infant>
    		</Header>
    		<FlightSegment>
    			<flight_id>{request_data.flight_id}</flight_id>
    			<fare_id>{request_data.fare_id or ''}</fare_id>
    			<origin_rcd>{request_data.origin}</origin_rcd>
    			<destination_rcd>{request_data.destination}</destination_rcd>
    		</FlightSegment>
		</Booking>"""
        
        payload = f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
      <tem:FlightAdd>
         <tem:strXml>
         <![CDATA[
         {inner_xml}
		]]>
         </tem:strXml>
      </tem:FlightAdd>
   </soapenv:Body>
</soapenv:Envelope>"""

        cookies = self.session_store.get(search_id)
        if not cookies:
             search_logger.warning(f"No cookies found for search_id={search_id} in FlightAdd. Session might be invalid.")

        async with httpx.AsyncClient(cookies=cookies) as client:
            try:
                search_logger.info(f"Sending FlightAdd request to {self.url} for search_id={search_id} flight_id={request_data.flight_id}")
                self.log_to_file(search_id, "FlightAdd_RQ.xml", payload)
                
                response = await client.post(self.url, headers=self.headers, content=payload, timeout=30.0)
                response.raise_for_status()
                
                if response.cookies:
                    self.session_store[search_id] = response.cookies

                search_logger.info(f"Received response from Yeti API FlightAdd: status={response.status_code}")
                self.log_to_file(search_id, "FlightAdd_RS.xml", response.text)
                return response.text
            except httpx.HTTPError as e:
                search_logger.error(f"Yeti API error in FlightAdd: {e}")
                raise Exception(f"Yeti API error in FlightAdd: {e}")

    async def booking_get_session(self, search_id: str):
        search_logger = get_search_logger(search_id)
        
        payload = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
      <tem:BookingGetSession/>
   </soapenv:Body>
</soapenv:Envelope>"""

        cookies = self.session_store.get(search_id)

        async with httpx.AsyncClient(cookies=cookies) as client:
            try:
                search_logger.info(f"Sending BookingGetSession request to {self.url} for search_id={search_id}")
                self.log_to_file(search_id, "BookingGetSession_RQ.xml", payload)
                
                response = await client.post(self.url, headers=self.headers, content=payload, timeout=30.0)
                response.raise_for_status()
                
                if response.cookies:
                    self.session_store[search_id] = response.cookies

                search_logger.info(f"Received response from Yeti API BookingGetSession: status={response.status_code}")
                self.log_to_file(search_id, "BookingGetSession_RS.xml", response.text)
                return response.text
            except httpx.HTTPError as e:
                search_logger.error(f"Yeti API error in BookingGetSession: {e}")
                raise Exception(f"Yeti API error in BookingGetSession: {e}")

    async def booking_save(self, request_data, search_id: str):
        search_logger = get_search_logger(search_id)
        
        passengers_xml = ""
        for p in request_data.passengers:
            passengers_xml += f"""
                <Passenger>
                    <passenger_id>{p.passenger_id}</passenger_id>
                    <passenger_type_rcd>{p.passenger_type_rcd}</passenger_type_rcd>
                    <lastname>{p.lastname}</lastname>
                    <firstname>{p.firstname}</firstname>
                    <gender_type_rcd>{p.gender_type_rcd}</gender_type_rcd>
                    <nationality_rcd>{p.nationality_rcd}</nationality_rcd>
                    <date_of_birth>{p.date_of_birth}</date_of_birth>
                </Passenger>"""

        inner_xml = f"""<Booking>
                <BookingHeader>
                    <contact_name>{request_data.booking_header.contact_name}</contact_name>
                    <contact_email>{request_data.booking_header.contact_email}</contact_email>
                    <phone_mobile>{request_data.booking_header.phone_mobile}</phone_mobile>
                    <phone_home>{request_data.booking_header.phone_home or ''}</phone_home>
                    <phone_business>{request_data.booking_header.phone_business or ''}</phone_business>
                </BookingHeader>
                {passengers_xml}
                <Payment>
                    <form_of_payment_rcd>{request_data.payment.form_of_payment_rcd}</form_of_payment_rcd>
                    <currency_rcd>{request_data.payment.currency_rcd}</currency_rcd>
                    <payment_amount>{request_data.payment.payment_amount}</payment_amount>
                </Payment>
            </Booking>"""
        
        payload = f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
      <tem:BookingSave>
         <tem:strXml>
            <![CDATA[
            {inner_xml}
            ]]>
         </tem:strXml>
      </tem:BookingSave>
   </soapenv:Body>
</soapenv:Envelope>"""

        cookies = self.session_store.get(search_id)

        async with httpx.AsyncClient(cookies=cookies) as client:
            try:
                search_logger.info(f"Sending BookingSave request to {self.url} for search_id={search_id}")
                self.log_to_file(search_id, "BookingSave_RQ.xml", payload)
                
                response = await client.post(self.url, headers=self.headers, content=payload, timeout=30.0)
                response.raise_for_status()
                
                if response.cookies:
                    self.session_store[search_id] = response.cookies

                search_logger.info(f"Received response from Yeti API BookingSave: status={response.status_code}")
                self.log_to_file(search_id, "BookingSave_RS.xml", response.text)
                return response.text
            except httpx.HTTPError as e:
                search_logger.error(f"Yeti API error in BookingSave: {e}")
                raise Exception(f"Yeti API error in BookingSave: {e}")

    async def booking_get_itinerary(self, pnr: str, search_id: str):
        search_logger = get_search_logger(search_id)
        
        payload = f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/">
   <soapenv:Header/>
   <soapenv:Body>
      <tem:BookingGetItinerary>
         <tem:strRecordLocator>{pnr}</tem:strRecordLocator>
      </tem:BookingGetItinerary>
   </soapenv:Body>
</soapenv:Envelope>"""

        cookies = self.session_store.get(search_id)

        async with httpx.AsyncClient(cookies=cookies) as client:
            try:
                search_logger.info(f"Sending BookingGetItinerary request to {self.url} for search_id={search_id} pnr={pnr}")
                self.log_to_file(search_id, "BookingGetItinerary_RQ.xml", payload)
                
                response = await client.post(self.url, headers=self.headers, content=payload, timeout=30.0)
                response.raise_for_status()

                if response.cookies:
                    self.session_store[search_id] = response.cookies

                search_logger.info(f"Received response from Yeti API BookingGetItinerary: status={response.status_code}")
                self.log_to_file(search_id, "BookingGetItinerary_RS.xml", response.text)
                return response.text
            except httpx.HTTPError as e:
                search_logger.error(f"Yeti API error in BookingGetItinerary: {e}")
                raise Exception(f"Yeti API error in BookingGetItinerary: {e}")

yeti_client = YetiClient()
