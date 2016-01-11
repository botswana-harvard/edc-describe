from django import template

register = template.Library()


@register.assignment_tag
def update_cumulative_frequency(this_value, running_total, forloop_counter=0):
    if forloop_counter == 1:
        running_total = this_value
    else:
        running_total += this_value
    return running_total


@register.assignment_tag
def update_total(aggregates):
    if not isinstance(aggregates, list):
        raise TypeError('Templatetag update_total expected type list. Got type %s' % type(aggregates))
    my_total = 0
    for aggregate in aggregates:
        my_total = my_total + aggregate['count']
    return my_total
