request flow:
client sends request->api key checked->event type validated against enum->db session opens->query runs->rows convert to pydantic models->serialized to json->response sent->session closes

threat model:
.env is git ignored, api key required in header for endpoints, no sql injection possible since no raw sql, pydantic models declare specific fields, so nothing extra can leave