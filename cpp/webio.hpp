#include <unordered_map>
#include "elements.hpp"

namespace webio {

class Rendering {
  int element_index_counter = 0;
  std::unordered_map<int, std::function<void(void)>> registered_actions;
  FrontEndElement& frame;
  Rendering(FrontEndElement& frame) {
    this->frame = EvaluateFrame(frame);
  }
  int GetUniqueIndex() {
    element_index_counter += 1;
    return element_index_counter;
  }
  FrontEndElement& EvaluateFrame(FrontEndElement& frame) {
    return frame;
  }
};

// class ErrorCodes {
//   CLIENT_INSTANCE_TIMEOUT = 1
//   INCORRECT_SERVER_INSTANCE = 2
//   INTERNAL_ERROR = 3
//   SUCCESS = 4
//   INVALID_ACTION = 5
//   INCOMPLETE_INPUT_VALUES = 6
// };

template<typename T>
class FrameServer {
  using ServingClassType = T;
  struct ClientInstance {
    ServingClassType client_instance;
    FrontEndElement current_frame;
  };
  unordered_map<int, ClientInstance> client_instances;
  int client_instance_id_counter = 1;
  FrameServer() {}

  int CreateClientInstance() {
    ubt instance_id = client_instance_id_counter++;
    client_instances[instance_id] = ClientInstance(ServingClassType());
    return instance_id;
  }

  void ReloadFrame(int instance_id) {
    auto& instance = client_instances.at(instance_id);
    auto raw_rendered = instance.client_instance.Render();
    instance.current_frame = Rendering(raw_rendered);
    instance.recent_active_timestamp = utils.GetEpochTimenow();
    return instance.current_frame.frame.Export();
  }

  string HandleFirstTimeLoad() {
    client_instance_id = self.CreateClientInstance();
    output = Object(
      error = Object(error_code = ErrorCodes.SUCCESS.__str__()),
      data = self.ReloadFrame(client_instance_id),
      client_instance_id = client_instance_id,
      server_instance_id = self.server_instance_id,
    );
    return output;
  }


  def PopulateInputs(self, instance_id, inputs):
    inputs = dict((int(k), v) for k,v in inputs.items());
    output_findall = Object();
    instance = self.client_instances[instance_id];
    def PopulateInputsHelper(nodes):
      output = Object();
      for node in nodes:
        if (type(node[1]) != list):
          input_value = instance.current_frame.CreateInputValue(node[1],
                                                                inputs[node[1]]);
          if node[0] not in output_findall:
            output_findall[node[0]] = [];
          output_findall[node[0]].append(input_value);
          output.update({node[0]: input_value});
        else:
          output.update({node[0]: PopulateInputsHelper(node[1])});
      return output;
    output = PopulateInputsHelper(instance.current_frame.input_acceser);
    instance.client_instance.inputs = output;
    instance.client_instance.all_inputs = output_findall;

  def HandleActionEvent(self, input_data):
    output = Object(error = Object(error_code = ErrorCodes.SUCCESS.__str__()));
    instance_id = input_data["client_instance_id"];
    if input_data["server_instance_id"] != self.server_instance_id:
      output.error.error_code = ErrorCodes.INCORRECT_SERVER_INSTANCE.__str__();
    elif instance_id not in self.client_instances:
      output.error.error_code = ErrorCodes.CLIENT_INSTANCE_TIMEOUT.__str__();
    else:
      instance = self.client_instances[instance_id];
      current_frame = instance.current_frame;
      if input_data.get("action_id") not in current_frame.registered_actions:
        output.error.error_code = ErrorCodes.INVALID_ACTION.__str__();
      else:
        try:
          self.PopulateInputs(instance_id, input_data.get('inputs', {}));
          current_frame.registered_actions[input_data["action_id"]]();
          output.error.error_code = ErrorCodes.SUCCESS.__str__();
          output.data = self.ReloadFrame(instance_id);
        except Exception as e:
          error_trace = traceback.format_exc();
          print(error_trace);
          output.error.error_code = ErrorCodes.INTERNAL_ERROR.__str__();
    return output;

  def CleanupOldInstancesIfRequired(self):
    timenow = utils.GetEpochTimenow();
    if (timenow > self.last_instance_clean_timestamp
                  + Configs.client_instance_cleaner_frequency):
      old_client_instances = [];
      for i,v in self.client_instances.items():
        if (utils.GetEpochTimenow() >
              Configs.client_instance_timeout + v.recent_active_timestamp):
          old_client_instances.append(i);
      list(self.client_instances.pop(i) for i in old_client_instances);
      print("[cleanup] deleted client_instances ", old_client_instances);
      self.last_instance_clean_timestamp = timenow;

  def Run(self, port):
    self.last_instance_clean_timestamp = utils.GetEpochTimenow();
    app = flask.Flask("webio");
    @app.route("/", methods = ["GET"])
    @flask_cors.cross_origin(supports_credentials = True)
    def v1_start():
      self.CleanupOldInstancesIfRequired();
      front_end_dir = os.path.join(os.path.dirname(__file__), 'front_end')
      html_page = read_file(front_end_dir + "/index.html");
      html_page = html_page.replace(
        '<!-- {inlined_css_here:template_arg_0} -->',
        "<style>" + read_file(front_end_dir + "/css/main.css")+"</style>")
      html_page = html_page.replace('tmp_frame_6703[1]',
                                    json.dumps(self.HandleFirstTimeLoad()));
      return html_page;

    @app.route("/v1/api", methods=["POST"])
    def v1_api():
      return flask.Response(
        response = json.dumps(self.HandleActionEvent(flask.request.json)),
        mimetype = "application/json"
      );

    app.run(port = port, debug = True);

def Serve(cls, args=[], params={}, port = 5018):
  return FrameServer(cls, args, params).Run(port = port);



}  // namespace webio