"""                                                                                                      
Copyright 2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.                                  
                                                                                                         
Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at                                              
                                                                                                         
    http://aws.amazon.com/apache2.0/                                                                     
                                                                                                         
or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.                                                 
"""

import cfn_flip
import json
import unittest

class ValidateTestCase(unittest.TestCase):
    """
    Test that the validator works correctly
    """

    def setUp(self):
        """
        Load in the examples and pre-parse the expected results
        """

        with open("examples/test.json", "r") as f:
            self.input_json = f.read()

        self.parsed_json = json.loads(self.input_json)

    def test_valid(self):
        """
        Test that valid data passes ok
        """

        self.assertTrue(cfn_flip.validate(self.parsed_json))

    def test_bad_data(self):
        """
        Test we fail on invalid data type
        """

        with self.assertRaisesRegex(cfn_flip.ValidationError, "Badly formatted input"):
            cfn_flip.validate("This should be a dict")

    def test_missing_resources(self):
        """
        Test we fail on missing resources
        """

        with self.assertRaisesRegex(cfn_flip.ValidationError, "Missing \"Resources\" property"):
            cfn_flip.validate({})

    def test_bad_resource(self):
        """
        Test we fail on a badly-formatted resource
        """

        source = {
            "Resources": {
                "Test": {},
            },
        }

        with self.assertRaisesRegex(cfn_flip.ValidationError, "Badly formatted resource: Test"):
            cfn_flip.validate(source)

    def test_invalid_resource_type(self):
        """
        Test we fail on missing resources
        """

        source = {
            "Resources": {
                "Test": {
                    "Type": "AWS::Cutlery::Spoon",
                },
            },
        }

        with self.assertRaisesRegex(cfn_flip.ValidationError, "Resource \"Test\" has invalid type: AWS::Cutlery::Spoon"):
            cfn_flip.validate(source)

    def test_missing_properties(self):
        """
        Test for missing properties
        """

        source = {
            "Resources": {
                "Test": {
                    "Type": "AWS::EC2::Instance",
                },
            },
        }

        with self.assertRaisesRegex(cfn_flip.ValidationError, "Resource \"Test\" has missing required properties: ImageId"):
            cfn_flip.validate(source)

    def test_unexpected_properties(self):
        """
        Test for missing properties
        """

        source = {
            "Resources": {
                "Test": {
                    "Type": "AWS::EC2::Instance",
                    "Properties": {
                        "ImageId": "GladOS-0.1",
                        "Cake": "lie",
                        "WeightInKilograms": 10,
                    },
                },
            },
        }

        with self.assertRaisesRegex(cfn_flip.ValidationError, "Resource \"Test\" has unexpected properties: Cake, WeightInKilograms"):
            cfn_flip.validate(source)
