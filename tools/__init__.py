from tools.mls_tool import create_request_to_mls
from langchain_core.tools import tool


@tool
def mls_tool(total_area: int, address: str, total_bedrooms: int, total_bathrooms: int):
    """Useful for when you need to collect data from the MLS to give valuation of the estate.
        The input to this tool should be four property data with values about numbers of bedrooms,
        bathrooms, total_area and address from the user input.
        That tool will allow you to collect the data from the MLS storage, and then you should return to the user
        the highest, lowest and average prices per square foot in that area.
        The answer can be rephrased to more human-like answer"""
    return create_request_to_mls(total_area, address, total_bedrooms, total_bathrooms)
