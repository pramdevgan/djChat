from django.db.models import Count
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.response import Response

from .models import Server
from .schema import server_list_docs
from .serializer import ServerSerializer


class ServerListViewSet(viewsets.ViewSet):
    """
    # ServerListViewSet

    A viewset for listing servers with various filtering options.

    This viewset allows users to retrieve a list of servers with optional filters based on category, user membership, the number of members, quantity, and server ID. It supports both basic and advanced queries to cater to different use cases.
    """

    queryset = Server.objects.all()

    @server_list_docs
    def list(self, request):
        """
        Retrieves a list of servers based on query parameters with various filtering options.

        This method processes the query parameters from the request and filters the queryset of servers accordingly. The filtered server data is then serialized and returned as a response.

        ## Args:
        &nbsp;&nbsp;&nbsp;&nbsp; **request (rest_framework.request.Request):** The HTTP request object.

        ## Returns:
        &nbsp;&nbsp;&nbsp;&nbsp; **rest_framework.response.Response:** A Response object containing the serialized server data.

        ## Raises:
        - AuthenticationFailed: If 'by_user' is set to 'true' and the user is not authenticated.
        - ValidationError: If the server ID provided in 'by_serverid' is invalid or does not exist.

        ## Query Parameters:
        - `category` (str, optional): Filter servers by category name.
        - `by_user` (bool, optional): Filter servers by user membership (requires authentication).
        - `qty` (int, optional): Limit the number of servers to be returned.
        - `by_serverid` (int, optional): Filter servers by a specific server ID.
        - `with_num_members` (bool, optional): Include the number of members in the response.

        ## Example Usage:
        - To retrieve a list of servers in a specific category: </br>
           &nbsp;&nbsp; **GET** */api/servers/?category=MyCategory*
        - To get servers where the current user is a member: </br>
           &nbsp;&nbsp; **GET** */api/servers/?by_user=true*
        - Retrieve the first 10 servers: </br>
           &nbsp;&nbsp; **GET** */api/servers/?qty=10*
        - Filter servers by a specific server ID: </br>
           &nbsp;&nbsp; **GET** */api/servers/?by_serverid=42*
        - Include the number of members for each server in the response: </br>
           &nbsp;&nbsp; **GET** */api/servers/?with_num_members=true*

        ## Additional Details:
        - The `category` parameter filters servers by their assigned category name.
        - Setting `by_user` to 'true' restricts the query to servers the current user is a member of.
        - Use the `qty` parameter to limit the number of servers returned.
        - The `by_serverid` parameter filters by a specific server's ID, which should be a valid integer.
        - Enabling `with_num_members` includes the count of members in the response.

        # Note:
        &nbsp;&nbsp;&nbsp;&nbsp;***This function is designed for querying and retrieving a list of servers with various filters.***
        """
        # Extract query parameters
        category = request.query_params.get("category")
        by_user = request.query_params.get("by_user") == "true"
        qty = request.query_params.get("qty")
        by_serverid = request.query_params.get("by_serverid")
        with_num_members = request.query_params.get("with_num_members") == "true"

        # Apply filters based on query parameters
        if category:
            self.queryset = self.queryset.filter(category__name=category)

        if by_user:
            # Handle authentication check
            if by_user and request.user.is_authenticated:
                user_id = request.user.id
                self.queryset = self.queryset.filter(member=user_id)
            else:
                raise AuthenticationFailed
        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count("member"))

        if qty:
            self.queryset = self.queryset[: int(qty)]

        if by_serverid:
            # Handle authentication check
            if not request.user.is_authenticated:
                raise AuthenticationFailed()

            try:
                self.queryset = self.queryset.filter(id=by_serverid)
                if not self.queryset.exists():
                    raise ValidationError(
                        detail=f"Server with ID {by_serverid} does not exist"
                    )
            except ValueError:
                raise ValidationError(detail=f"Invalid server ID")

        # Serialize the data and return as a response
        serializer = ServerSerializer(
            self.queryset, many=True, context={"num_members": with_num_members}
        )
        return Response(serializer.data)
