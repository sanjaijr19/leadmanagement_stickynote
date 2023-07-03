# from datetime import timezone
from django.utils import timezone

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Lead
from .serializers import LeadSerializer
from rest_framework import viewsets, generics, status


# Create your views here.

class LeadView(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    lookup_field = 'id'


class LeadCreateView(generics.CreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer


class LeadListView(generics.ListAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer


class LeadRetrieveView(generics.RetrieveAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    lookup_field = 'id'


class LeadUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    lookup_field = 'id'

    # def put(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save(edited_on=timezone.now())  # Update the edited_on field
    #     return Response(serializer.data)


class LeadDeleteView(generics.RetrieveDestroyAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    lookup_field = 'id'


class LeadCategoryViewSet(generics.CreateAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

    # def post(self, request):
    #     lead_source = request.data.get('lead_source')
    #
    #     if Lead.objects.filter(lead_source=lead_source).exists():
    #         return Response(dict(resp="error", resp_msg="Selected Category Does Not Exist", resp_code="101"),
    #                         status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         Lead.objects.create(lead_source=lead_source)


        # if not ProductServiceCategory.objects.filter(tenant_id=tenant.id, id=category_id).exists():
        #     return Response(dict(resp="error", resp_msg="Selected Category Does Not Exist", resp_code="101"),
        #                     status=status.HTTP_400_BAD_REQUEST)
        # product_ids = json.loads(products)
        # for proId in product_ids:
        #     try:
        #         product = Product.objects.get(productId=proId, tenant=tenant)
        #         product.prod_cat_id = category_id
        #         product.device = get_device_object(tenant=tenant, dev_id=device)
        #         product.save()
        #     except Product.DoesNotExist:
        #         pass
        #
        # return Response(dict(resp="success", resp_msg="Items added to Category successfully", resp_code="001"),
        #                 status=status.HTTP_200_OK)