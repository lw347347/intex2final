from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import Campaign
from api.serializers import CampaignSerializer
from api.serializers import CampaignSearchSerializer
# from api.models import Donation
# from api.serializers import DonationSerializer
# from api.models import Update
# from api.serializers import UpdateSerializer

import json
import stripe
import math


########################
###  Campaign

class CampaignList(APIView):
    @csrf_exempt
    def get(self, request, format=None):
        cats = Campaign.objects.all()
        if request.query_params.get('campaign_id'):
            cats = cats.filter(campaign_id__contains=request.query_params.get('campaign_id'))
        if request.query_params.get('category'):
            cats = cats.filter(category__contains=request.query_params.get('category'))
        if request.query_params.get('current_amount'):
            # Check if they want more or less than
            if request.query_params.get('current_amount_more_than'):
                # They want to get those that are more than or equal to
                cats = cats.filter(current_amount__gte=request.query_params.get('current_amount'))
            else:
                # They want less than or equal to
                cats = cats.filter(current_amount__lte=request.query_params.get('current_amount'))
        if request.query_params.get('goal'):
             # Check if they want more or less than
            if request.query_params.get('goal_more_than') == True:
                # They want to get those that are more than or equal to
                cats = cats.filter(goal__gte=request.query_params.get('goal'))
            else:
                # They want less than or equal to
                cats = cats.filter(goal__lte=request.query_params.get('goal'))
        if request.query_params.get('donators'):
             # Check if they want more or less than
            if request.query_params.get('donators_more_than'):
                # They want to get those that are more than or equal to
                cats = cats.filter(donators__gte=request.query_params.get('donators'))
            else:
                # They want less than or equal to
                cats = cats.filter(donators__lte=request.query_params.get('donators'))
        if request.query_params.get('days_active'):
            # Check if they want more or less than
            if request.query_params.get('days_active_more_than'):
                # They want to get those that are more than or equal to
                cats = cats.filter(days_active__gte=request.query_params.get('days_active'))
            else:
                # They want less than or equal to
                cats = cats.filter(days_active__lte=request.query_params.get('days_active'))
        if request.query_params.get('title'):
            cats = cats.filter(title__contains=request.query_params.get('title'))
        if request.query_params.get('has_beneficiary'):
            cats = cats.filter(title__contains=request.query_params.get('has_beneficiary'))
        if request.query_params.get('user_id'):
            cats = cats.filter(title__contains=request.query_params.get('user_id'))
        if request.query_params.get('created_at'):
            # Check if they want more or less than
            if request.query_params.get('created_at_more_than'):
                # They want to get those that are more than or equal to
                cats = cats.filter(created_at__gte=request.query_params.get('created_at'))
            else:
                # They want less than or equal to
                cats = cats.filter(created_at__lte=request.query_params.get('created_at'))
        if request.query_params.get('launch_date'):
            # Check if they want more or less than
            if request.query_params.get('launch_date_more_than'):
                # They want to get those that are more than or equal to
                cats = cats.filter(launch_date__gte=request.query_params.get('launch_date'))
            else:
                # They want less than or equal to
                cats = cats.filter(launch_date__lte=request.query_params.get('launch_date'))
        if request.query_params.get('campaign_hearts'):
            # Check if they want more or less than
            if request.query_params.get('campaign_hearts_more_than'):
                # They want to get those that are more than or equal to
                cats = cats.filter(campaign_hearts__gte=request.query_params.get('campaign_hearts'))
            else:
                # They want less than or equal to
                cats = cats.filter(campaign_hearts__lte=request.query_params.get('campaign_hearts'))
        if request.query_params.get('social_share_total'):
            # Check if they want more or less than
            if request.query_params.get('social_share_total_more_than'):
                # They want to get those that are more than or equal to
                cats = cats.filter(social_share_total__gte=request.query_params.get('social_share_total'))
            else:
                # They want less than or equal to
                cats = cats.filter(social_share_total__lte=request.query_params.get('social_share_total'))
        if request.query_params.get('location_city'):
            cats = cats.filter(title__contains=request.query_params.get('location_city'))
        if request.query_params.get('location_country'):
            cats = cats.filter(title__contains=request.query_params.get('location_country'))
        if request.query_params.get('is_charity'):
            cats = cats.filter(title__contains=request.query_params.get('is_charity'))
        if request.query_params.get('charity_valid'):
            cats = cats.filter(title__contains=request.query_params.get('charity_valid'))
        if request.query_params.get('charity_npo_id'):
            cats = cats.filter(title__contains=request.query_params.get('charity_npo_id'))
        if request.query_params.get('charity_name'):
            cats = cats.filter(title__contains=request.query_params.get('charity_name'))
        
        serializer = CampaignSerializer(cats, many=True)
        return Response(serializer.data)

    @csrf_exempt
    def post(self, request, format=None):
        serializer = CampaignSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CampaignSearch(APIView):
    @csrf_exempt
    def get(self, request, format=None):
        cats = Campaign.objects.all()
        if request.query_params.get('campaign_id'):
            cats = cats.filter(campaign_id__contains=request.query_params.get('campaign_id'))
        if request.query_params.get('category'):
            cats = cats.filter(category__contains=request.query_params.get('category'))
        if request.query_params.get('current_amount'):
            # Check if they want more or less than
            if request.query_params.get('current_amount_less_than') == 'true':
                # They want to get those that are less than or equal to
                cats = cats.filter(current_amount__lte=request.query_params.get('current_amount'))
            else:
                # They want greater than or equal to
                cats = cats.filter(current_amount__gte=request.query_params.get('current_amount'))
        if request.query_params.get('goal'):
             # Check if they want more or less than
            if request.query_params.get('goal_less_than') == 'true':
                # They want to get those that are less than or equal to
                cats = cats.filter(goal__lte=request.query_params.get('goal'))
            else:
                # They want more than or equal to
                cats = cats.filter(goal__gte=request.query_params.get('goal'))
        if request.query_params.get('donators'):
             # Check if they want more or less than
            if request.query_params.get('donators_less_than') == 'true':
                # They want to get those that are less than or equal to
                cats = cats.filter(donators__lte=request.query_params.get('donators'))
            else:
                # They want more than or equal to
                cats = cats.filter(donators__gte=request.query_params.get('donators'))
        if request.query_params.get('days_active'):
            # Check if they want more or less than
            if request.query_params.get('days_active_less_than') == 'true':
                # They want to get those that are less than or equal to
                cats = cats.filter(days_active__lte=request.query_params.get('days_active'))
            else:
                # They want more than or equal to
                cats = cats.filter(days_active__gte=request.query_params.get('days_active'))
        if request.query_params.get('title'):
            cats = cats.filter(title__contains=request.query_params.get('title'))
        if request.query_params.get('has_beneficiary') == 'true' and request.query_params.get('does_not_have_beneficiary') == 'true':
            # Do nothing
            x = 1
        elif request.query_params.get('has_beneficiary') == 'false' and request.query_params.get('does_not_have_beneficiary') == 'false':
            # Do nothing 
            x = 1
        elif request.query_params.get('has_beneficiary') == 'true':
            # filter down
            cats = cats.filter(has_beneficiary__contains='TRUE')
        elif request.query_params.get('does_not_have_beneficiary') == 'true':
            # filter down
            cats = cats.filter(has_beneficiary__contains='FALSE')
        if request.query_params.get('user_id'):
            cats = cats.filter(title__contains=request.query_params.get('user_id'))
        if request.query_params.get('created_at'):
            # Check if they want more or less than
            if request.query_params.get('created_at_less_than'):
                # They want to get those that are less than or equal to
                cats = cats.filter(created_at__lte=request.query_params.get('created_at'))
            else:
                # They want more than or equal to
                cats = cats.filter(created_at__gte=request.query_params.get('created_at'))
        if request.query_params.get('launch_date'):
            # Check if they want more or less than
            if request.query_params.get('launch_date_less_than'):
                # They want to get those that are less than or equal to
                cats = cats.filter(launch_date__lte=request.query_params.get('launch_date'))
            else:
                # They want more than or equal to
                cats = cats.filter(launch_date__gte=request.query_params.get('launch_date'))
        if request.query_params.get('campaign_hearts'):
            # Check if they want more or less than
            if request.query_params.get('campaign_hearts_less_than') == 'true':
                # They want to get those that are less than or equal to
                cats = cats.filter(campaign_hearts__lte=request.query_params.get('campaign_hearts'))
            else:
                # They want more than or equal to
                cats = cats.filter(campaign_hearts__gte=request.query_params.get('campaign_hearts'))
        if request.query_params.get('social_share_total'):
            # Check if they want more or less than
            if request.query_params.get('social_share_total_less_than') == 'true':
                # They want to get those that are less than or equal to
                cats = cats.filter(social_share_total__lte=request.query_params.get('social_share_total'))
            else:
                # They want more than or equal to
                cats = cats.filter(social_share_total__gte=request.query_params.get('social_share_total'))
        if request.query_params.get('location_city'):
            cats = cats.filter(title__contains=request.query_params.get('location_city'))
        if request.query_params.get('location_country'):
            cats = cats.filter(title__contains=request.query_params.get('location_country'))
        if request.query_params.get('is_charity') == 'true' and request.query_params.get('is_not_charity') == 'true':
            # Do nothing
            x = 1
        elif request.query_params.get('is_charity') == 'false' and request.query_params.get('is_not_charity') == 'false':
            # Do nothing 
            x = 1
        elif request.query_params.get('is_charity') == 'true':
            # filter down
            cats = cats.filter(is_charity__contains='TRUE')
        elif request.query_params.get('is_not_charity') == 'true':
            # filter down
            cats = cats.filter(is_charity__contains='FALSE')
        if request.query_params.get('charity_valid') == 'true':
            cats = cats.filter(charity_valid__contains='TRUE')
        if request.query_params.get('charity_valid') == 'true' and request.query_params.get('charity_not_valid') == 'true':
            # Do nothing
            x = 1
        elif request.query_params.get('charity_valid') == 'false' and request.query_params.get('charity_not_valid') == 'false':
            # Do nothing 
            x = 1
        elif request.query_params.get('charity_valid') == 'true':
            # filter down
            cats = cats.filter(charity_valid__contains='TRUE')
        elif request.query_params.get('charity_not_valid') == 'true':
            # filter down
            cats = cats.filter(charity_valid__contains='FALSE')
        if request.query_params.get('charity_npo_id'):
            cats = cats.filter(title__contains=request.query_params.get('charity_npo_id'))
        if request.query_params.get('charity_name'):
            cats = cats.filter(title__contains=request.query_params.get('charity_name'))
        
        serializer = CampaignSearchSerializer(cats, many=True)
        return Response(serializer.data)

    @csrf_exempt
    def post(self, request, format=None):
        serializer = CampaignSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CampaignDetail(APIView):
    '''Work with an individual Campaign object'''
    @csrf_exempt
    def get(self, request, pk, format=None):
        cat = Campaign.objects.get(campaign_id=pk)
        serializer = CampaignSerializer(cat)
        return Response(serializer.data)

    @csrf_exempt
    def put(self, request, pk, format=None):
        cat = Campaign.objects.get(campaign_id=pk)
        serializer = CampaignSerializer(cat, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @csrf_exempt
    def delete(self, request, pk, format=None):
        cat = Campaign.objects.get(campaign_id=pk)
        cat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PredictionCalculator(APIView):
    @csrf_exempt
    def get(self, request, format=None):
    # this view receives parameters from the submit html template and calls the API in azure
    # this contains API code for Python and Python3 

        # If you are using Python 3+, import urllib instead of urllib2
        #import urllib2.request
        import urllib
        import json 

        # Grab the inputs from formik
        campaign_id = '0'
        goal = request.query_params.get('goal')
        title = request.query_params.get('title') + ' value'
        description = request.query_params.get('description')
        has_beneficiary = request.query_params.get('has_beneficiary')
        visible_in_search = request.query_params.get('visible_in_search')
        is_charity = request.query_params.get('is_charity')
        npo_id = request.query_params.get('npo_id')
        is_individual = request.query_params.get('is_individual')
        description_language = request.query_params.get('description_language')
        creator_type = '0'

        # Grab the inputs from formik for the donations calculator
        auto_fb_post_mode = request.query_params.get('auto_fb_post_mode')
        currencycode = request.query_params.get('currencycode')
        user_facebook_id = request.query_params.get('user_facebook_id')
        location_country = request.query_params.get('location_country')


        # Determine creator type
        if is_individual == 'true':
            creator_type = '0'
        elif npo_id:
            creator_type = '1'
        elif is_charity == 'true':
            creator_type = '2'
        else:
            creator_type = '0'

        # Change has beneficiary to number
        if has_beneficiary == 'true':
            has_beneficiary = '1'
        else:
            has_beneficiary = '0'

        # Change visible in search to number
        if visible_in_search == 'true':
            visible_in_search = '1'
        else:
            visible_in_search = '0'

        # Change auto_fb_post_mode to number
        if auto_fb_post_mode == 'true':
            auto_fb_post_mode = '1'
        else:
            auto_fb_post_mode = '0'

        # Change user_facebook_id to number
        if user_facebook_id == 'true':
            user_facebook_id = '1'
        else:
            user_facebook_id = '0'

        # assign all the parameters to variables which you put in the API like the commented code
        # or just put them in directly like I did farther down
        
        # age = str(request.POST['age'])
        # sex = str(request.POST['sex'])
        # bmi = str(request.POST['bmi'])
        # children = str(request.POST['children'])
        # smoker = str(request.POST['smoker'])
        # region = str(request.POST['region'])
        
        donorData =  {
                    "Inputs": {
                        "input1": {
                        "ColumnNames": [
                            "auto_fb_post_mode",
                            "currencycode",
                            "goal",
                            "title",
                            "description",
                            "has_beneficiary",
                            "user_facebook_id",
                            "visible_in_search",
                            "location_country",
                            "creator_type",
                            "description Language"
                        ],
                        "Values": [
                            [
                            auto_fb_post_mode,
                            currencycode,
                            goal,
                            title,
                            description,
                            has_beneficiary,
                            user_facebook_id,
                            visible_in_search,
                            location_country,
                            creator_type,
                            description_language
                            ]
                        ]
                        }
                    },
                    "GlobalParameters": {}
                    }
        # the API call
        body = str.encode(json.dumps(donorData))
        url = 'https://ussouthcentral.services.azureml.net/workspaces/b7fcea30955b4e65baaa8dfa89044435/services/27397440e0f04626b791a9fd2257b2c8/execute?api-version=2.0&details=true'
        api_key = 'h4A9kOn6xELpLbA+ouvOMEl6MY2C5Pca0LMJl7XCc9fUh/6ike1zAYL3/iQzbN8zfY2F0rIUxUHxkJVAkGQpHQ=='
        # Replace my url and api_key with your own values
        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

        # If you are using Python 3+, replace urllib2 with urllib.request
        #req = urllib2.Request(url, body, headers)
        req = urllib.request.Request(url, body, headers) 

        # python3 uses urllib while python uses urllib2
        #response = urllib2.request.urlopen(req)
        response = urllib.request.urlopen(req)

        # this formats the results 
        result = response.read()
        result = json.loads(result) # turns bits into json object
        numberOfDonors = result["Results"]["output1"]["value"]["Values"][0][0] 

        # formatting the data into a data object for the API call
        data =  {
                "Inputs": {
                    "input1": {
                    "ColumnNames": [
                        "campaign_id",
                        "goal",
                        "title",
                        "description",
                        "has_beneficiary",
                        "visible_in_search",
                        "creator_type",
                        "description Language"
                    ],
                    "Values": [
                        [
                        campaign_id,
                        goal,
                        title,
                        description,
                        has_beneficiary,
                        visible_in_search,
                        creator_type,
                        description_language
                        ]
                    ]
                    }
                },
                "GlobalParameters": {}
                }

        # the API call
        body = str.encode(json.dumps(data))
        url = 'https://ussouthcentral.services.azureml.net/workspaces/b7fcea30955b4e65baaa8dfa89044435/services/d67343eff77f4da8816f310ad22f74f3/execute?api-version=2.0&details=true'
        api_key = 'eznkftQu4cspVH/yRkW07L5CXI8itN/q3AeQyKryesI35MT61KXEGs6gjFQaTWizGqlYgcazuR+tC3VlO8B4ww=='
        # Replace my url and api_key with your own values
        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

        # If you are using Python 3+, replace urllib2 with urllib.request
        #req = urllib2.Request(url, body, headers)
        req = urllib.request.Request(url, body, headers) 

        # python3 uses urllib while python uses urllib2
        #response = urllib2.request.urlopen(req)
        response = urllib.request.urlopen(req)

        # this formats the results 
        result = response.read()
        result = json.loads(result) # turns bits into json object
        totalPercentOfGoal = result["Results"]["output1"]["value"]["Values"][0][0] 
        
        # Reverse the transformation that we had in Azure
        totalPercentOfGoal = totalPercentOfGoal = float(totalPercentOfGoal)**6

        # Reverse the transformation that we had in Azure
        numberOfDonors = math.exp(float(numberOfDonors))
        
        # Make the response to send back to React
        totalAmount = str(round((float(totalPercentOfGoal) * float(goal)), 2))
        amountPerDonor = str(round((float(totalAmount) / float(numberOfDonors)), 2))
        responseForReact = [totalAmount, totalPercentOfGoal, numberOfDonors, amountPerDonor]
        
        # serializer = PredictionCalculatorSerializer(cats, many=True)
        return Response(responseForReact)