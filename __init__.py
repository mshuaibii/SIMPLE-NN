import yaml 
import collections

# TODO: logging

def deep_update(source, overrides):
    """
    Update a nested dictionary or similar mapping.
    Modify ``source`` in place.
    """
    for key in overrides.keys():
        if isinstance(source, collections.Mapping):
            if isinstance(overrides[key], collections.Mapping) and overrides[key]:
                returned = deep_update(source.get(key, {}), overrides[key])
                source[key] = returned
            # Need list append?
            else:
                source[key] = overrides[key]
        else:
            source = {key: overrides[key]}
    return source

class simple_nn(object):
    def __init__(self, inputs, descriptor=None, model=None):
        """
        inputs: filename which contains YAML style input parameters
        descriptor, model
        """
        self.inputs = dict()
        if descriptor != None:
            self.descriptor = descriptor
            self.inputs = deep_update(self.inputs, self.descriptor.default_inputs)

        if model != None:
            self.model = model
            self.inputs = deep_update(self.inputs, self.model.default_inputs)

        self.inputs = deep_update(self.inputs, yaml.load(open(inputs)))

        if not 'atom_types' in self.inputs:
            raise KeyError
        
        self.logfile = open('LOG', 'w', 10)

    def _log_header(self):
        # TODO: make the log header (low priority)
        self.logfile.write("SIMPLE_NN\n")

    @property
    def inputs(self):
        return self._inputs

    @inputs.setter
    def inputs(self, inputs):
        self._inputs = inputs

    @property
    def descriptor(self):
        return self._descriptor

    @descriptor.setter
    def descriptor(self, descriptor):
        descriptor.parent = self
        self._descriptor = descriptor
        self._descriptor.inputs = self.inputs['neural_network']

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model):
        model.parent = self
        self._model = model


    #def log(self, message):
    #    self._log.write(message)

    def run(self, user_optimizer=None):
        self.descriptor.generate()
        self.model.train(user_optimizer=user_optimizer)
