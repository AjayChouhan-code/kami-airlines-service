from django.template.loader import render_to_string

from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.openapi import Contact, Info, License
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    Info(
        title="Kami Airlines Service API's",
        default_version="v1",
        description="The KAMI Airlines Service is a Python-based solution designed to address the aircraft passenger capacity issue for KAMI Airlines. It includes functional code with simple setup and execution instructions to solve the passenger booking and capacity problem.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=Contact(email="contact@snippets.local"),
        license=License(name="BSD License"),
    ),
    public=True,
)


class CustomCodeAutoSchema(SwaggerAutoSchema):
    """
    This class inherits the base class ``SwaggerAutoSchema`` and it includes ``get_operation`` method to generate 'x-code-samples' for endpoints documentation.
    """

    def __init__(self, view, path, method, components, request, overrides, yasg):
        """
        A constructor method for a custom code auto schema class.
        """
        super().__init__(view, path, method, components, request, overrides)

    def get_operation(self, operation_keys):
        """
        This method gets an Operation for the given API endpoint (path, method).
        This includes query, body parameters, and response schemas.

        :param  operation_keys: an array of keys describing the hierarchical layout of this view in the API  e.g.; ``('snippets', 'list')``, ``('snippets', 'retrieve')``, etc.
        :type operation_keys: tuple[str]
        :returns: operation
        :rtype: openapi.Operation
        """
        operation = super(CustomCodeAutoSchema, self).get_operation(operation_keys)

        # Using django templates to generate the code
        template_context = {
            "request_url": "https://{hostname}" + self.path,
            "method": self.method,
        }
        operation.update(
            {
                "x-code-samples": [
                    {
                        "lang": "curl",
                        "source": render_to_string(
                            "curl_sample.html", template_context
                        ),
                    },
                    {
                        "lang": "python",
                        "source": render_to_string(
                            "python_sample.html", template_context
                        ),
                    },
                ]
            }
        )
        return operation
