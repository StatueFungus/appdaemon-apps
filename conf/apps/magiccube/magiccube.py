import hassapi as hass

class MagicCube(hass.Hass):
    
    def initialize(self):
        self.listen_state(self.state_changed, self.args["entity_id"], attribute = "all")


    def state_changed(self, entity, attribute, old, new, kwargs):
        if new["state"] != '' and new["attributes"]["action"] != '':
            self.log(new, level="DEBUG")
            self.handle_cube_event(new["attributes"]["action"])


    def handle_cube_event(self, action):
        if "actions" in self.args and action in self.args["actions"]:
            action_arguments_list = self.args["actions"][action]
            for action_arguments in action_arguments_list:
                self.log("Perform action with argument: " + str(action_arguments))
                self.peform_action(action_arguments)


    def peform_action(self, action_arguments):
        if "action" not in action_arguments:
            return
        
        action = action_arguments["action"]

        if action == "toggle":
            self.perform_entity_action(action_arguments, self.toggle)
        elif action == "turn_on":
            self.perform_entity_action(action_arguments, self.turn_on)
        elif action == "turn_off":
            self.perform_entity_action(action_arguments, self.turn_off)
        elif action == "call_service":
            self.perform_service_call(action_arguments)
        elif action == "cycle_scene":
            self.perform_cycle_scene(action_arguments)
        
    def perform_entity_action(self, action_arguments, function):
        entity = action_arguments["entity"]
        function(entity)


    def perform_service_call(self, action_arguments):
        service = action_arguments["service"]
        service_args = action_arguments["service_args"]

        self.call_service(service, **service_args)


    def perform_cycle_scene(self, action_arguments):
        scene_entity = action_arguments["scene_selection"]
        direction = action_arguments["scene_cycle"]

        if direction == "next":
            self.call_service("input_select/select_next", entity_id=scene_entity)
        else:
            self.call_service("input_select/select_previous", entity_id=scene_entity)

        #scene_selection = self.get_entity("input_select.arbeitszimmer_szenenwahl")
        scene_selection = self.get_entity(scene_entity)

        active_scene_id = scene_selection.get_state()
        self.call_service("scene/turn_on", entity_id=active_scene_id, transition=1)
