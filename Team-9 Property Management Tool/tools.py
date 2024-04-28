import httpx
from pydantic import BaseModel, Field


class DovecPriceFinder(BaseModel):
    minPrice: int
    maxPrice: int

class DovecFinder(BaseModel):
    prop_no: str = Field(..., title="Properties", description="If users ask about all properties, you should check the properties list and return the all properties")

class FilePathSchema(BaseModel):
    filePath: str = Field(..., title="Filepath", description="File path required")

class OccupancyStatusFinder(BaseModel):
    occupancy_status: str = Field(..., title="Occupancy Status", description="Occupancy status required, status are: "
                                                                             "Occupied, Vacant and Under Renovation. "
                                                                             "Occupied and Under Renovation is busy, "
                                                                             "Vacant is available")

class PropertyTypeFinder(BaseModel):
    property_type: str = Field(..., title="Property Type", description="Type of property required, property types "
                                                                       "are: Apartment, Commercial, Single Family "
                                                                       "Home and Mixed-Use.")

class UnitsFinder(BaseModel):
    number_of_units: int = Field(..., title="Number of Units", description="Number of units required")

async def check_number_of_units(number_of_units: int):
    try:
        url = "https://api.npoint.io/488527433ae8fb2f1ce1/"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  # Check for HTTP errors
            data = response.json()  # Convert JSON data to Python dict
            # Filter properties by the specified number of units
            filtered_properties = [(property, property['Number_of_Units']) for property in data
                                   if property.get('Number_of_Units') and int(property['Number_of_Units']) == number_of_units]
            return filtered_properties
    except httpx.HTTPStatusError as e:
        print(f"HTTP Error: {e}")
    except httpx.RequestError as e:
        print(f"Request Error: {e}")
    except Exception as e:
        print(f"Other Error: {e}")

async def check_property_type(property_type: str):
    try:
        url = "https://api.npoint.io/488527433ae8fb2f1ce1/"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  # Check for HTTP errors
            data = response.json()  # Convert JSON data to Python dict
            # Filter properties by the specified property type
            filtered_properties = [(prop, prop['Property_Type'], prop['Number_of_Units']) for prop in data
                                   if prop.get('Property_Type', '').casefold() == property_type.casefold()]
            return filtered_properties
    except httpx.HTTPStatusError as e:
        print(f"HTTP Error: {e}")
    except httpx.RequestError as e:
        print(f"Request Error: {e}")
    except Exception as e:
        print(f"Other Error: {e}")


async def check_occupancy_status(occupancy_status: str):
    try:
        url = "https://api.npoint.io/488527433ae8fb2f1ce1/"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  # Check for HTTP errors
            data = response.json()  # Convert JSON data to Python dict
            # Filter properties by the specified occupancy status
            filtered_properties = [(property, property['Occupancy_Status']) for property in data
                                   if property.get('Occupancy_Status').casefold() == occupancy_status.casefold()]
            return filtered_properties
    except httpx.HTTPStatusError as e:
        print(f"HTTP Error: {e}")
    except httpx.RequestError as e:
        print(f"Request Error: {e}")
    except Exception as e:
        print(f"Other Error: {e}")

async def dovec_finder(prop_no: str):
    url = "https://api.npoint.io/488527433ae8fb2f1ce1"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

async def dovec_price_finder(minPrice: int, maxPrice: int):
    try:
        url = f"https://api.npoint.io/488527433ae8fb2f1ce1/"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  # HTTP hatalarını kontrol et
            data = response.json()  # JSON verisini al ve dönüştür
            # minPrice ve maxPrice aralığında olan mülkleri filtreleyin
            filtered_properties = [(property['Location'], property['Rental_Price']) for property in data if
                                   property.get('Rental_Price') and minPrice <= int(property['Rental_Price']) <= maxPrice]
            return filtered_properties
    except httpx.HTTPStatusError as e:
        print(f"HTTP Hatası: {e}")
    except httpx.RequestError as e:
        print(f"İstek Hatası: {e}")
    except Exception as e:
        print(f"Diğer Hata: {e}")

def custom_json_schema(model):
    schema = model.schema()
    properties_formatted = {
        k: {
            "title": v.get("title"),
            "type": v.get("type")
        } for k, v in schema["properties"].items()
    }

    return {
        "type": "object",
        "default": {},
        "properties": properties_formatted,
        "required": schema.get("required", [])
    }

tools = [
{
        "name": "Dovec_Price_Finder",
        "description": "This function takes min price, max price or both min and max prices, returning all properties "
                       "about that price range, so whenever your receiving a min price or max price you're going to "
                       "return me all of the properties related to this price range",
        "parameters": custom_json_schema(DovecPriceFinder),
        "runCmd": dovec_price_finder,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": True,
        "rerunWithDifferentParameters": True
    },
{
        "name": "Dovec_Unit_Finder",
        "description": "This function takes numbers of unit, returning all properties with numbers of units, so whenever your receiving number of unit request you're going to return me all of the properties with number of units",
        "parameters": custom_json_schema(UnitsFinder),
        "runCmd": check_number_of_units,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": True,
        "rerunWithDifferentParameters": True
    },
{
        "name": "Dovec_Type_Finder",
        "description": "This function takes property type, returning all properties about that property type, so whenever your receiving a property type you're going to return me all of the properties related to this property type",
        "parameters": custom_json_schema(PropertyTypeFinder),
        "runCmd": check_property_type,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": True,
        "rerunWithDifferentParameters": True
    },
{
        "name": "Dovec_Occupy_Finder",
        "description": "This function checks occupancy status, returning all properties about that occupancy status, so whenever your receiving an occupancy request you're going to return me all of the properties related to this occupancy status",
        "parameters": custom_json_schema(OccupancyStatusFinder),
        "runCmd": check_occupancy_status,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": True,
        "rerunWithDifferentParameters": True
    },
{
        "name": "Dovec_Finder",
        "description": "This function takes property number and returns all information about that property, so whenever your receiving a property number you're going to return me all of the information related to this property, this must be checked Property_ID from the data",
        "parameters": custom_json_schema(DovecFinder),
        "runCmd": dovec_finder,
        "isDangerous": False,
        "functionType": "backend",
        "isLongRunningTool": False,
        "rerun": True,
        "rerunWithDifferentParameters": True
    }
]
