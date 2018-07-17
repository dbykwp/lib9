
from .Capacity import Capacity
from .Farmer import Farmer
from .api_response import APIResponse
from .unhandled_api_error import UnhandledAPIError
from .unmarshall_error import UnmarshallError


class ApiService:
    def __init__(self, client):
        self.client = client

    def RegisterFarmer(self, headers=None, query_params=None, content_type="application/json"):
        """
        Register a farmer
        It is method for GET /api/farmer_create
        """
        uri = self.client.base_url + "/api/farmer_create"
        return self.client.get(uri, None, headers, query_params, content_type)

    def UpdateFarmer(self, headers=None, query_params=None, content_type="application/json"):
        """
        Update a farmer
        It is method for GET /api/farmer_update
        """
        uri = self.client.base_url + "/api/farmer_update"
        return self.client.get(uri, None, headers, query_params, content_type)

    def GetFarmer(self, iyo_organization, headers=None, query_params=None, content_type="application/json"):
        """
        Get detail about a farmer
        It is method for GET /api/farmers/{iyo_organization}
        """
        uri = self.client.base_url + "/api/farmers/" + iyo_organization
        resp = self.client.get(uri, None, headers, query_params, content_type)
        try:
            if resp.status_code == 200:
                return APIResponse(data=Farmer(resp.json()), response=resp)

            message = 'unknown status code={}'.format(resp.status_code)
            raise UnhandledAPIError(response=resp, code=resp.status_code,
                                    message=message)
        except ValueError as msg:
            raise UnmarshallError(resp, msg)
        except UnhandledAPIError as uae:
            raise uae
        except Exception as e:
            raise UnmarshallError(resp, e.message)

    def ListFarmers(self, headers=None, query_params=None, content_type="application/json"):
        """
        List Farmers
        It is method for GET /api/farmers
        """
        uri = self.client.base_url + "/api/farmers"
        resp = self.client.get(uri, None, headers, query_params, content_type)
        try:
            if resp.status_code == 200:
                resps = []
                for elem in resp.json():
                    resps.append(Farmer(elem))
                return APIResponse(data=resps, response=resp)

            message = 'unknown status code={}'.format(resp.status_code)
            raise UnhandledAPIError(response=resp, code=resp.status_code,
                                    message=message)
        except ValueError as msg:
            raise UnmarshallError(resp, msg)
        except UnhandledAPIError as uae:
            raise uae
        except Exception as e:
            raise UnmarshallError(resp, e.message)

    def RecordCapacityBeat(self, data, headers=None, query_params=None, content_type="application/json"):
        """
        Record capacity beat
        It is method for POST /api/nodes/beat
        """
        uri = self.client.base_url + "/api/nodes/beat"
        resp = self.client.post(uri, data, headers, query_params, content_type)
        try:
            if resp.status_code == 201:
                return APIResponse(data=Capacity(resp.json()), response=resp)

            message = 'unknown status code={}'.format(resp.status_code)
            raise UnhandledAPIError(response=resp, code=resp.status_code,
                                    message=message)
        except ValueError as msg:
            raise UnmarshallError(resp, msg)
        except UnhandledAPIError as uae:
            raise uae
        except Exception as e:
            raise UnmarshallError(resp, e.message)

    def GetCapacity(self, node_id, headers=None, query_params=None, content_type="application/json"):
        """
        Get detail about capacity of a node
        It is method for GET /api/nodes/{node_id}
        """
        uri = self.client.base_url + "/api/nodes/" + node_id
        resp = self.client.get(uri, None, headers, query_params, content_type)
        try:
            if resp.status_code == 200:
                return APIResponse(data=Capacity(resp.json()), response=resp)

            message = 'unknown status code={}'.format(resp.status_code)
            raise UnhandledAPIError(response=resp, code=resp.status_code,
                                    message=message)
        except ValueError as msg:
            raise UnmarshallError(resp, msg)
        except UnhandledAPIError as uae:
            raise uae
        except Exception as e:
            raise UnmarshallError(resp, e.message)

    def ListCapacity(self, headers=None, query_params=None, content_type="application/json"):
        """
        List all the nodes capacity
        It is method for GET /api/nodes
        """
        uri = self.client.base_url + "/api/nodes"
        resp = self.client.get(uri, None, headers, query_params, content_type)
        try:
            if resp.status_code == 200:
                resps = []
                for elem in resp.json():
                    resps.append(Capacity(elem))
                return APIResponse(data=resps, response=resp)

            message = 'unknown status code={}'.format(resp.status_code)
            raise UnhandledAPIError(response=resp, code=resp.status_code,
                                    message=message)
        except ValueError as msg:
            raise UnmarshallError(resp, msg)
        except UnhandledAPIError as uae:
            raise uae
        except Exception as e:
            raise UnmarshallError(resp, e.message)

    def RegisterCapacity(self, data, headers=None, query_params=None, content_type="application/json"):
        """
        Register a node capacity
        It is method for POST /api/nodes
        """
        uri = self.client.base_url + "/api/nodes"
        resp = self.client.post(uri, data, headers, query_params, content_type)
        try:
            if resp.status_code == 201:
                return APIResponse(data=Capacity(resp.json()), response=resp)

            message = 'unknown status code={}'.format(resp.status_code)
            raise UnhandledAPIError(response=resp, code=resp.status_code,
                                    message=message)
        except ValueError as msg:
            raise UnmarshallError(resp, msg)
        except UnhandledAPIError as uae:
            raise uae
        except Exception as e:
            raise UnmarshallError(resp, e.message)
