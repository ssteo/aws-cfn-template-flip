"""                                                                                                      
Copyright 2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.                                  
                                                                                                         
Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at                                              
                                                                                                         
    http://aws.amazon.com/apache2.0/                                                                     
                                                                                                         
or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.                                                 
"""

import json

SPEC_FILE = "cfn_flip/CloudFormationResourceSpecification.json"

class ValidationError(Exception):
    pass

with open(SPEC_FILE, "r") as f:
    SPEC = json.load(f)

def validate_get_att(resource_name, attribute, source):
    """
    Confirm that the specificied resource has the attribute in question
    """

    return True

def validate_ref(ref_name, source):
    """
    Confirm that the specified ref is valid
    """

    return True

def validate_properties(resource_name, properties, spec, source):
    """
    Compare the specified properties against the supplied spec.
    The entire source must be passed in to ensure that references etc are valid
    """

    # Check required parameters
    required = [key for key, value in spec.items() if value["Required"]]
    missing = [key for key in required if key not in properties]
    if missing:
        raise ValidationError("Resource \"{}\" has missing required properties: {}".format(resource_name, ", ".join(missing)))

    # Check for unexpected parameters
    unexpected = [key for key in properties if key not in spec]
    if unexpected:
        raise ValidationError("Resource \"{}\" has unexpected properties: {}".format(resource_name, ", ".join(sorted(unexpected))))

def validate_resource(resource_name, source):
    """
    Confirm that the resource is valid.
    The entire source must be passed in to ensure that references etc are valid
    """

    resource = source["Resources"][resource_name]

    if "Type" not in resource:
        raise ValidationError("Badly formatted resource: {}".format(resource_name))

    if resource["Type"] not in SPEC["ResourceTypes"]:
        raise ValidationError("Resource \"{}\" has invalid type: {}".format(resource_name, resource["Type"]))

    validate_properties(resource_name, resource.get("Properties", {}), SPEC["ResourceTypes"][resource["Type"]]["Properties"], source)

def validate(source):
    """
    Confirm that the source conforms to the cloudformation spec
    """

    if not isinstance(source, dict):
        raise ValidationError("Badly formatted input")

    if "Resources" not in source:
        raise ValidationError("Missing \"Resources\" property")

    for resource_name in source["Resources"].keys():
        validate_resource(resource_name, source)

    return True
