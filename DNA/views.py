from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from DNA.main import *

context = {}


def format_result(values, res):
    format = 'Input: \n'
    for val in values:
        format += val + ' -> ' + (str(0), str(1))[values[val]] + '\n'
    format += 'Output: ' + (str(0), str(1))[res]
    print(format)
    return format

def index(request):
    global context

    if request.method != 'POST':
        context = {
            'correct': True,
            'circuit_input': '',
            'pressed': False,
            'get_res_pressed': False,
            'result': False
        }

    if request.method == 'POST' and 'check' in request.POST:
        logic = request.POST.get('circuit')
        reset()
        correct = check_correctness(logic)
        context['circuit_input'] = logic
        context['correct'] = correct
        context['pressed'] = True
        context['result'] = ''
        context['values'] = {}
        if correct:
            reset()
            circuit = parse(logic)
            draw_graph(circuit)
            context['vars'] = variables
        return render(request, 'DNA/main.html', context)
    elif request.method == 'POST' and 'get_res' in request.POST:
        for var in variables:
            values[var] = (False, True)[request.POST.get(var) == '1']
        circuit = parse(request.POST.get('circuit'))
        result = DNA_computing_simulation(replace_to_nand_logic(circuit), values)
        context['result'] = format_result(values, result)
        context['correct'] = True
        context['pressed'] = True
        context['get_res_pressed'] = True
        context['values'] = values
        return render(request, 'DNA/main.html', context)
    return render(request, 'DNA/main.html', context)
