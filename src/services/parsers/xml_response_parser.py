"""XML response parser implementation."""
from typing import Dict, Any
from src.services.interfaces.response_parser import IResponseParser
from src.utils.xml_parser import parse_yeti_xml_response


class XmlResponseParser(IResponseParser):
    """Parser for XML responses from Yeti service."""
    
    def parse(self, raw_response: str) -> Dict[str, Any]:
        """Parse XML response to dictionary."""
        return parse_yeti_xml_response(raw_response)
