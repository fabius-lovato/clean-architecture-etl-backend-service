from google.cloud.datastore import Client

class GCPDatastoreConnection:
    __singleton = None
    __gcp_client = None

    def __new__(cls):
        if cls.__singleton is None:
            cls.__singleton = object.__new__(cls)

        return cls.__singleton

    def __init__(self):
        if self.__gcp_client is None:
            credential_info: str = self.__get_credentials()
            self.__gcp_client = Client.from_service_account_info(credential_info)

    def __get_credentials(self) -> dict:
        # TODO: Obter as credenciais através da variável de ambiente `GOOGLE_APPLICATION_CREDENTIALS`
        credentials = {
            "type": "service_account",
            "project_id": "gcp-default-project-404622",
            "private_key_id": "ae05ddcf863a8073b1c0b97880cfaba2de80edcc",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDCv/UsBTPkIqnL\nsx2ImdStexxMRYy7I0XXaMTUxFo4Uk9Q8SCfr5TtjYcBu+JCedmNF6rABSs41ZBi\nZmLoYkWwEe+muYmxezYsyaXM8+PSeep9s8kOdRni2b2VIm1xezPRPBOFRiYGxZLU\nBREG2pvrL+l1tInZlm9mt2B4T6Fh/nVJ2OoidYWDd5Wmf9srn7osw0g7X/ma2/Ip\n4QHgB++ugifa3S+Fu3bgeP6nfYcXo4bDXycT/pPtLAdxmpufj99v8XKDGsKQFkhs\nRQr6KMOQB4AqBFBr3L6obEk19TU7SdroDwtTc+5sPo6Pa7k0k/Zq2iMFZbaAzUXl\nX24tEukbAgMBAAECggEAQJsHjWPoc/0f0OiJmqBVknttxsunxQkNiUlDSsYcm+SK\nVXK4fOD1idzSdbvLcnwTtJ+uUGcmkIMgk9QdabP4JFG+69NPH2adcTwv2Y7q/A7f\nwHWc9EPao4vSPaAfKG9ToEzKuQKtaL+wVs+bd2ecI+hQDXEn7dve9vdMdH0OL4By\nUC0pKZXjKmYBzxRv693i2BpQZMevkFNuSg/v5XCJwT5uM1WJa9dD9/i9zB1BKtL+\nDMkdzoyWep5+93b17ev/ecJt37o/Atw431iOgbU6kRk3eJV+w9AbmIq/4EJXtL00\nXi0P2WGVReZCjLoCRW4U0S5eed38R41mmlDNJATZgQKBgQD8KyjYgHKmTfBl7tyJ\n50M1b4NFIc+jcR7o5adpZjxbLuznC9EVNZCMXPenlBxei5K4djuz5PM3hefAcI1/\noROPamtawxz5OzM00FB/4PEQx3g2hrfL5RTNEwDSX7LH57hFXuacF9cadVXEIUXH\nANOEkDOHt+EC2tlOXezjxHLOwQKBgQDFtXX9m0mAT6SZDitgnjf16KaaCtUWMHxN\nReT1He72LKlQAFQlIUKA7LHSCyjz+4+lwz1ZEh7QGhsCysT1mORQ/W99NpNqDxUH\nfG21r346MSLMSKHDtRr23OzayG7dw8wRuNp10lbRZ1Sk810ls2Z1FtGc6cdeuICb\nBC/XfWiK2wKBgBBDrF/CcSKe1kmMzXarjt8scRgNZToSer7kyRZ4PJ5Y+Xixf2vR\nx5/2Axcw61+BuxXgslsZAkLrhRYZbFb2Ca/vWjtBaGX+1n+qi/ajiIjfhLZnnAUv\nolbTyfLHr11Lacw3ocIhm4MeXEjJKJn8SKg9MMWpK38mpGt0jWnnasxBAoGABtwv\nBee3ey5IRc9KDgYvZub1sO6jSivQhFXihebN/di63z3Dra4jwplz6hfdCeo2p8fI\nfyizzQC64zPp9aOieHTyw2N7Zfi0ABh/Lgiy1o4R6Qi0JDhKgTpVNZoyzpsWn57M\nZb4wqP9u3nJbTw2UhoeOKmWqN00rmTVh+5YsZHUCgYEAmJK5ellDQzMFItU2leJE\nnvsxZr2o3N6supOCuT9nHksj74oxM88lMgSo74BYUKoOpDdxdMYsdAOKNdNJSDJG\nPGl0GCHSJWK8vny3w0GTRPcVTF5a5U2r4FpHqPhSsDvxxLBN6AreOws5qfVGiEBS\n8rZZRSoREbWIf50nJbLxRhE=\n-----END PRIVATE KEY-----\n",
            "client_email": "main-service-account@gcp-default-project-404622.iam.gserviceaccount.com",
            "client_id": "105734626496073408208",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/main-service-account%40gcp-default-project-404622.iam.gserviceaccount.com",
            "universe_domain": "googleapis.com"
            }

        return credentials

    def client(self) -> Client:
        return self.__gcp_client
