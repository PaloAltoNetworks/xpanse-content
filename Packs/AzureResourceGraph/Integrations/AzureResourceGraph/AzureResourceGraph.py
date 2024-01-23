import demistomock as demisto  # noqa: F401
from CommonServerPython import *  # noqa: F401
from MicrosoftApiModule import *  # noqa: E402

'''GLOBAL VARS'''
API_VERSION = '2022-10-01'
APP_NAME = 'azure-resource-graph'


class AzureResourceGraphClient:
    """
      Azure Resource Graph Client enables authorized access to query for resource information.
      """

    def __init__(self, tenant_id, auth_id, enc_key, app_name, base_url, verify, proxy, self_deployed, ok_codes, server,
                 subscription_id, certificate_thumbprint, private_key):

        self.ms_client = MicrosoftClient(
            tenant_id=tenant_id, auth_id=auth_id, enc_key=enc_key, app_name=app_name, base_url=base_url, verify=verify,
            proxy=proxy, self_deployed=self_deployed, ok_codes=ok_codes, scope=Scopes.management_azure,
            certificate_thumbprint=certificate_thumbprint, private_key=private_key,
            command_prefix="azure-rg",
        )

        self.server = server
        self.subscription_id = subscription_id
        self.default_params = {"api-version": API_VERSION}

    def list_operations(self):
        return self.ms_client.http_request(
            method='GET',
            full_url=f"{self.server}/providers/Microsoft.ResourceGraph/operations",
            params=self.default_params,
        )

    def query_resources(self, query):
        request_data = {"query": query}
        return self.ms_client.http_request(
            method='POST',
            full_url=f"{self.server}/providers/Microsoft.ResourceGraph/resources",
            params=self.default_params,
            json_data=request_data
        )


def query_resources_command(client: AzureResourceGraphClient, args: dict[str, Any]) -> CommandResults:
    query = args.get('query')
    response = client.query_resources(query)

    query_data = response.get('data')

    title = f"Results of query:\n```{query}```"
    human_readable = tableToMarkdown(title, query_data, removeNull=True)

    return CommandResults(
        readable_output=human_readable,
        outputs_prefix='AzureResourceGraph.Query',
        outputs_key_field='Query',
        outputs=query_data,
        raw_response=response
    )


def list_operations_command(client: AzureResourceGraphClient, args: dict[str, Any]) -> CommandResults:
    limit = arg_to_number(args.get('limit')) or 50

    response = client.list_operations()
    value = response.get('value')

    operations = []
    for operation in value[:limit]:
        operation_context = {
            'Name': operation.get('name'),
            'Display': operation.get('display')
        }
        operations.append(operation_context)

    title = 'List of Azure Resource Graph Operations'
    human_readable = tableToMarkdown(title, operations, removeNull=True)

    return CommandResults(
        readable_output=human_readable,
        outputs_prefix='AzureResourceGraph.Operations',
        outputs_key_field='Operations',
        outputs=operations,
        raw_response=response
    )


def test_module(client: AzureResourceGraphClient):
    # Implicitly will test tenant, enc_token and subscription_id
    try:
        result = client.list_operations()
        if result:
            return 'ok'
    except DemistoException as e:
        return_error(f"Test connection failed with message {e}")


def main():
    params: dict = demisto.params()
    args = demisto.args()
    server = params.get('host', 'https://management.azure.com').rstrip('/')
    tenant = params.get('cred_token', {}).get('password') or params.get('tenant_id')
    auth_and_token_url = params.get('cred_auth_id', {}).get('password') or params.get('auth_id')
    if not tenant or not auth_and_token_url:
        return_error('Token and ID must be provided.')
    enc_key = params.get('cred_enc_key', {}).get('password') or params.get('enc_key')
    certificate_thumbprint = params.get('cred_certificate_thumbprint', {}).get(
        'password') or params.get('certificate_thumbprint')
    private_key = params.get('private_key')
    verify = not params.get('unsecure', False)
    subscription_id = args.get('subscription_id') or params.get(
        'cred_subscription_id', {}).get('password') or params.get('subscription_id')
    proxy: bool = params.get('proxy', False)
    self_deployed: bool = params.get('self_deployed', False)
    if not self_deployed and not enc_key:
        raise DemistoException('Key must be provided. For further information see '
                               'https://xsoar.pan.dev/docs/reference/articles/microsoft-integrations---authentication')
    elif not enc_key and not (certificate_thumbprint and private_key):
        raise DemistoException('Key or Certificate Thumbprint and Private Key must be providedFor further information see '
                               'https://xsoar.pan.dev/docs/reference/articles/microsoft-integrations---authentication')
    ok_codes = (200, 201, 202, 204)

    commands_without_args: Dict[Any, Any] = {
        'test-module': test_module
    }

    commands_with_args: Dict[Any, Any] = {
        'azure-rg-query': query_resources_command,
        'azure-rg-list-operations': list_operations_command
    }

    commands_with_args_and_params: Dict[Any, Any] = {
    }

    '''EXECUTION'''
    command = demisto.command()
    LOG(f'Command being called is {command}')

    try:
        # Initial setup
        if not subscription_id:
            return_error('A subscription ID must be provided.')
        base_url = f"{server}/providers/Microsoft.ResourceGraph"

        client = AzureResourceGraphClient(
            base_url=base_url, tenant_id=tenant, auth_id=auth_and_token_url, enc_key=enc_key, app_name=APP_NAME,
            verify=verify, proxy=proxy, self_deployed=self_deployed, ok_codes=ok_codes, server=server,
            subscription_id=subscription_id, certificate_thumbprint=certificate_thumbprint,
            private_key=private_key)

        if command == 'azure-rg-auth-reset':
            return_results(reset_auth())

        elif command in commands_without_args:
            return_results(commands_without_args[command](client))

        elif command in commands_with_args:
            return_results(commands_with_args[command](client, args))

        elif command in commands_with_args_and_params:
            return_results(commands_with_args_and_params[command](client, args, params))

    except Exception as e:
        return_error(e)


if __name__ in ['__main__', 'builtin', 'builtins']:
    main()
