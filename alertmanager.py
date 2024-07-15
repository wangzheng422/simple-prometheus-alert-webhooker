from flask import Flask, request, jsonify
import json, subprocess
from queue import Queue

# Define a global queue
# alerts_queue = Queue()

app = Flask(__name__)

# Define the memory consumption threshold (in percentage)
DEF_MEMORY_THRESHOLD_PERCENT = 80  # Example threshold
# define alert name
# DEF_ALERT_NAME = "HighMemoryUsage"

def get_pod_ip(namespace, pod_name):
    # Corrected to use the provided namespace and pod_name parameters
    command = f"oc get pod {pod_name} -n {namespace} -o json"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if stderr:
        print(f"Error: {stderr.decode()}")
        return None

    # Parse the JSON output
    pod_info = json.loads(stdout)

    # Return the IP address of the specified pod
    return pod_info.get("status", {}).get("podIP", None)


@app.route('/alert', methods=['POST'])
def handle_alert():
    # Parse the incoming JSON data
    data = request.json
    print("Received data:", json.dumps(data, indent=4))  # Print the received JSON for debugging

    # here is the return json example
    # {
    #     "receiver": "llm-demo/example-routing/default",
    #     "status": "firing",
    #     "alerts": [
    #         {
    #             "status": "firing",
    #             "labels": {
    #                 "alertname": "HighMemoryUsage",
    #                 "namespace": "llm-demo",
    #                 "pod": "pod-description-writer-59b6b5d596-mfwbr",
    #                 "severity": "warning"
    #             },
    #             "annotations": {
    #                 "description": "Memory usage is above 80% (current value: 0.8564029693603515)",
    #                 "summary": "High Memory Usage"
    #             },
    #             "startsAt": "2024-07-15T05:09:09.031Z",
    #             "endsAt": "0001-01-01T00:00:00Z",
    #             "generatorURL": "https://thanos-querier-openshift-monitoring.apps.cluster-4wjr6.sandbox2771.opentlc.com/api/graph?g0.expr=%28sum+by+%28pod%29+%28container_memory_working_set_bytes%7Bcontainer%3D~%22.%2B%22%2Cnamespace%3D%22llm-demo%22%7D%29+%2F+sum+by+%28pod%29+%28kube_pod_container_resource_limits%7Bcontainer%3D~%22.%2B%22%2Cnamespace%3D%22llm-demo%22%7D%29%29+%3E+0.8+and+%28sum+by+%28pod%29+%28container_memory_working_set_bytes%7Bcontainer%3D~%22.%2B%22%2Cnamespace%3D%22llm-demo%22%7D%29+%2F+sum+by+%28pod%29+%28kube_pod_container_resource_limits%7Bcontainer%3D~%22.%2B%22%2Cnamespace%3D%22llm-demo%22%7D%29%29+%3C+9999&g0.tab=1",
    #             "fingerprint": "370261666f268ba9"
    #         }
    #     ],
    #     "groupLabels": {
    #         "pod": "pod-description-writer-59b6b5d596-mfwbr"
    #     },
    #     "commonLabels": {
    #         "alertname": "HighMemoryUsage",
    #         "namespace": "llm-demo",
    #         "pod": "pod-description-writer-59b6b5d596-mfwbr",
    #         "severity": "warning"
    #     },
    #     "commonAnnotations": {
    #         "description": "Memory usage is above 80% (current value: 0.8564029693603515)",
    #         "summary": "High Memory Usage"
    #     },
    #     "externalURL": "https://console-openshift-console.apps.cluster-4wjr6.sandbox2771.opentlc.com/monitoring",
    #     "version": "4",
    #     "groupKey": "{}/{namespace=\"llm-demo\"}:{pod=\"pod-description-writer-59b6b5d596-mfwbr\"}",
    #     "truncatedAlerts": 0
    # }

    # get namespace from commonLabels
    namespace = data['commonLabels']['namespace']
    # get pod name from commonLabels
    pod_name = data['commonLabels']['pod']
    # get alert name from commonLabels
    alert_name = data['commonLabels']['alertname']

    # if alert name is HighMemoryUsage, which is predefined
    # then, get pod_ip using oc command
    if alert_name == "HighMemoryUsage":
        pod_ip = get_pod_ip(namespace, pod_name)
        if pod_ip:
            print(f"Pod IP: {pod_ip}")
            # insert the json event into a python queue, with pod_ip and namespace as key
            # alerts_queue.put({'key': f"{pod_ip}_{namespace}", 'data': data})
        else:
            print("Pod IP not found or error occurred.")


    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)