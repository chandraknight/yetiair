import xmltodict
import html
import logging

logger = logging.getLogger(__name__)

def parse_yeti_xml_response(xml_string: str):
    """
    Parses the raw SOAP/XML response from Yeti API, unescapes the inner XML,
    and returns a structured dictionary.
    """
    try:
        # 1. Unescape HTML entities (converts &lt; to <, etc.)
        unescaped_xml = html.unescape(xml_string)
        
        # 2. Parse XML to Dict
        # Using xmltodict for easier handling of deep nested data
        # Note: xmltodict handles namespaces, which SOAP uses heavily.
        # We might want to strip namespaces or process specifically.
        parsed_dict = xmltodict.parse(unescaped_xml)
        
        # 3. Navigate to the relevant data node if possible
        # Usually: Envelope -> Body -> SpecificResponse -> SpecificResult
        # But since we unescaped the whole thing, the structure might be:
        # <soap:Envelope>...<soap:Body>...<Response>...<Result><ActualData>...</Result>...</Response>
        
        # Let's try to find the 'Body' content dynamically
        envelope = parsed_dict.get('soap:Envelope') or parsed_dict.get('soapenv:Envelope')
        if envelope:
            body = envelope.get('soap:Body') or envelope.get('soapenv:Body')
            if body:
                # return the first child of Body, which is the response wrapper
                # e.g., FlightAvailabilityResponse
                response_wrapper = list(body.values())[0] if body else {}
                # Inside wrapper, look for '...Result'
                # e.g., FlightAvailabilityResult
                for key, value in response_wrapper.items():
                    if key.endswith('Result'):
                        return value
                
                return response_wrapper
        
        return parsed_dict
        
    except Exception as e:
        logger.error(f"Error parsing Yeti XML response: {e}")
        # Return raw if parsing fails
        return {"raw_response": xml_string, "error": str(e)}

def unescape_xml(xml_string: str) -> str:
    """Helper to just unescape HTML entities for logging"""
    if not xml_string:
        return ""
    return html.unescape(xml_string)
