from cfnlint.rules import CloudFormationLintRule
from cfnlint.rules import RuleMatch


class RequiredTags(CloudFormationLintRule):
    """Check if Tags are present and have required keys"""
    id = 'E9000'
    shortdesc = 'Check if Tags are present and have required keys'
    description = 'Check Tags for resources'
    tags = ['resources', 'tags']

    def match(self, cfn):
        """Check if Tags are present and have required keys"""

        matches = []
        required_tags = ['env']

        all_resources = cfn.search_deep_keys('Properties')
        for resource in all_resources:
            if 'Tags' not in resource[-1]:
                message = "One or more tags ({0}) are missing on the resource: {1}".format(', '.join(required_tags), resource[:-1][1])
                matches.append(RuleMatch(resource, message))

        all_tags = [x for x in cfn.search_deep_keys('Tags') if x[0] == 'Resources']

        for all_tag in all_tags:
            all_keys = [d.get('Key') for d in all_tag[-1]]

            for required_tag in required_tags:
                if required_tag not in all_keys:
                    message = "Tag '{0}' missing for resource '{1}'"
                    matches.append(RuleMatch(all_tag[:-1], message.format(required_tag, all_tag[:-1][1])))

        return matches
