from cfnlint.rules import CloudFormationLintRule
from cfnlint.rules import RuleMatch
from cfnlint.helpers import RESOURCE_SPECS


class RequiredTags(CloudFormationLintRule):
    id = 'E9000'
    shortdesc = 'Check if Tags are present and have required keys'
    description = shortdesc
    tags = ['resources', 'tags']
    tags_to_check = ['env']

    def match(self, cfn):
        """Check Tags for required keys"""
        resource_types_with_tags = self.get_resource_types_with_tags(cfn.regions[0])
        resources = cfn.get_resources()

        matches = []
        for name, resource in resources.items():
            resource_type = resource.get('Type', '')
            if resource_type not in resource_types_with_tags:
                continue

            resource_properties = resource.get('Properties', {})
            tags = resource_properties.get('Tags', [])
            tags_dict = {i.get('Key'): i.get('Value') for i in tags}

            for tag in self.tags_to_check:
                if tag not in tags_dict:
                    matches.append(RuleMatch(
                        ['Resources', name, 'Properties', 'Tags'],
                        f'Missing tag "{tag}" for Resources/{name}',
                    ))

        return matches

    def get_resource_types_with_tags(self, region):
        all_resource_types = RESOURCE_SPECS[region]['ResourceTypes']

        resource_types = []
        for resource_type, resource in all_resource_types.items():
            properties = resource.get('Properties')
            if properties and 'Tags' in properties:
                resource_types.append(resource_type)
        return resource_types