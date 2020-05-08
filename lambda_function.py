import dateutil.parser
from botocore.vendored import requests


def lambda_handler(request, context):

    insert_nps_responses, last_nps_response_date = api_response(request['state'], request['secrets'])

    insert = dict()
    insert['nps_responses'] = insert_nps_responses

    delete = dict()
    delete['nps_responses'] = list()

    state = dict()
    state['nps_responsesCursor'] = last_nps_response_date

    nps_responses_schema = dict()
    nps_responses_schema['primary_key'] = ['id']

    schema = dict()
    schema['nps_responses'] = nps_responses_schema

    return dict(
        state=state,
        insert=insert,
        delete=delete,
        schema=schema,
        hasMore='false'
    )


def api_response(state, secrets):

    page = 1

    if 'nps_responsesCursor' in state:
        last_datetime_str = state['nps_responsesCursor']
        last_datetime = dateutil.parser.parse(last_datetime_str)
    else:
        last_datetime_str = None
        last_datetime = None

    if last_datetime is not None:
        add_request = dict(startDate=int(last_datetime.replace(microsecond=0).timestamp()))
    else:
        add_request = dict()

    new_datetime_str = last_datetime_str
    new_datetime = last_datetime

    return_data = list()

    while True:

        response = requests.get('https://app.retently.com/api/v2/nps/customers/response', dict(
            page=page,
            limit=50,
            sort='createdDate',
            **add_request
        ), headers={
            'Content-Type': 'application/json',
            'Authorization': f"api_key={secrets['api_key']}"
        })

        data = response.json()

        pages = data['data']['pages']

        if 'data' in data and 'responses' in data['data'] and len(data['data']['responses']) > 0:

            response_data = data['data']['responses']

            for datum in response_data:

                created_datetime = dateutil.parser.parse(datum['createdDate'])

                if new_datetime is None or created_datetime > new_datetime:

                    new_datetime = created_datetime
                    new_datetime_str = datum['createdDate']

                if last_datetime is None or created_datetime > last_datetime:
                    return_data.append(datum)

        else:
            break

        if page + 1 > pages:
            break

        page = page + 1

    return return_data, new_datetime_str
