from rest_framework.filters import (SearchFilter, # To make a search by variables
                                    OrderingFilter,
                                    )

from rest_framework.generics import (ListAPIView,  # To list all
                                     RetrieveAPIView,  # To retrieve specif
                                    )

from rest_framework.permissions import (IsAdminUser
                                        )

from regression.models import (Regression_ideal)

from regression.api.serializers import (RegressionListAllSerializer, RegressionPredictionsSerializer)

class PredictionApiAllIdealView(ListAPIView):  # To list all API VIEW
    # This one method allows make query
    filter_back_ends = [SearchFilter, OrderingFilter]
    search_fields = ['quantity']
    queryset = Regression_ideal.objects.all() #Whit only the second form of search this is commented
    serializer_class = RegressionListAllSerializer
    permission_classes = [IsAdminUser] # Authentication

    def list(self, request, *args, **kwargs):
        print(request.user)
        return super(PredictionApiAllIdealView, self).list(request, *args, **kwargs)

class PredictionApiRutIdealView(RetrieveAPIView):  # To retrieve by specific lookup_field API VIEW
    lookup_field = 'receptor_rut'
    queryset = Regression_ideal.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = RegressionPredictionsSerializer