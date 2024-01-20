#!/usr/bin/python3

MOVE_TO_THE_NEXT_STATE = 'MOVE_TO_THE_NEXT_STATE'
CHAT_EXIT = 'CHAT_EXIT'

class ChatContext:
    def __init__(self):
        self._context_data = {}
    
    def set(self, param, value):
        self._context_data[param] = value

    def get(self, param):
        return self._context_data[param]


class StateResult:
    def __init__(self, next_id, exit_code, data):
        self.next_id = next_id
        self.exit_code = exit_code
        self.data = data

class ChatState:
    def __init__(self):
        pass

    def process(self, data, context):
        pass

    def get_possible_exits(self):
        pass

class StartState(ChatState):
    def __init__(self):
        ChatState.__init__(self)

    def get_possible_exits(self):
        return ('read_name', )

    def process(self, data, context):
        print('Welcome into the chat. My name is ChatBot.')

        return StateResult('read_name', MOVE_TO_THE_NEXT_STATE, 'Please input your name:')

class ReadMessageState(ChatState):
    def __init__(self):
        ChatState.__init__(self)

    def get_possible_exits(self):
        return ('read_name', 'end_state', )

    def process(self, data, context):
        print('Enter your name: ', end="")
        message = input()

        context.set('MESSAGE', message)    

        if len(message) > 4:
            next_state = 'end_state'
        else:
            next_state = 'read_name'    
        return StateResult(next_state, MOVE_TO_THE_NEXT_STATE, 'Thank you!')

class EndState(ChatState):
    def __init__(self):
        ChatState.__init__(self)

    def get_possible_exits(self):
        return ( )

    def process(self, data, context):
        print('User name:', context.get('MESSAGE'))

        return StateResult('end_state', CHAT_EXIT, 'Bye!')

def main():
    start_state = StartState()

    chat_states = {}
    chat_states["start"] = start_state
    chat_states["read_name"] = ReadMessageState()
    chat_states["end_state"] = EndState()

    # render graph
    with open('chat_graph.txt','w') as graph_file: 
        graph_file.write('/* To view contents open the https://dreampuf.github.io/GraphvizOnline */\n')
        graph_file.write('digraph G {\n')
        for state_id in chat_states.keys():
            state = chat_states[state_id]

            for possible_next_state in state.get_possible_exits():
                graph_file.write( '%s -> %s;\n' % ( state_id, possible_next_state))

        graph_file.write('}')

    # chat cycle

    chat_context = ChatContext()

    state_result = start_state.process("Hello", chat_context) 

    while state_result.exit_code != CHAT_EXIT:
        next_state_input = state_result.data

        next_state = chat_states[state_result.next_id]
        state_result = next_state.process(next_state_input, chat_context)


if __name__ == "__main__":
    main()