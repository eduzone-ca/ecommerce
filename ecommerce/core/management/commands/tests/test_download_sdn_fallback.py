"""
Tests for Django management command to download csv for SDN fallback.
"""
from django.core.management import call_command
from django.core.management.base import CommandError
from mock import patch

from ecommerce.tests.testcases import TestCase


class TestDownloadSndFallbackCommand(TestCase):

    def setUp(self):
        class TestResponse:
            def __init__(self, **kwargs):
                self.__dict__ = kwargs

        #  mock response for csv download: just one row of the csv
        self.test_response = TestResponse(**{
            'content': bytes('_id,source,entity_number,type,programs,name,title,addresses,federal_register_notice,start_date,end_date,standard_order,license_requirement,license_policy,call_sign,vessel_type,gross_tonnage,gross_registered_tonnage,vessel_flag,vessel_owner,remarks,source_list_url,alt_names,citizenships,dates_of_birth,nationalities,places_of_birth,source_information_url,ids\ne5a9eff64cec4a74ed5e9e93c2d851dc2d9132d2,Denied Persons List (DPL) - Bureau of Industry and Security,,,, MICKEY MOUSE,,"123 S. TEST DRIVE, SCOTTSDALE, AZ, 85251",82 F.R. 48792 10/01/2017,2017-10-18,2020-10-15,Y,,,,,,,,,FR NOTICE ADDED,http://bit.ly/1Qi5heF,,,,,,http://bit.ly/1iwxiF0', 'utf-8'),  # pylint: disable=line-too-long
            'status_code': 200,
        })

    @patch('requests.Session.get')
    def test_with_mock_pass(self, mock_response):
        """ Test using mock response from setup, using threshold it will clear"""

        mock_response.return_value = self.test_response
        call_command('populate_sdn_fallback_data_and_metadata', '--threshold=0.0001')

    @patch('requests.Session.get')
    def test_with_mock_fail_size(self, mock_response):
        """ Test using mock response from setup, using threshold it will NOT clear"""

        mock_response.return_value = self.test_response
        with self.assertRaises(CommandError) as cm:
            call_command('populate_sdn_fallback_data_and_metadata', '--threshold=1')
        self.assertEqual('CSV file download did not meet threshold', str(cm.exception))

    def test_with_bad_url(self):
        """ Test using bad url, where connection exception occurs"""
        with self.assertRaises(CommandError) as cm:
            call_command('populate_sdn_fallback_data_and_metadata', '--threshold=1', '--url=http://googasdfle.com')
        self.assertEqual('Exception occurred', str(cm.exception))