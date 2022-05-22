from catalog import MBs, CPUs, VCs, RAMs, PSs
import secrets
import string


def generate_key_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    rand_string = ''.join(secrets.choice(letters_and_digits) for i in range(length))
    return rand_string

def generate_msg(list_part):
    result = f"Название: {list_part[0]}\n" \
             f"Описание: {list_part[2]}\n"\
             f"В наличии: {list_part[3]}\n"\
             f"Стоимость: {list_part[4]} ₽\n"
    return result  

def get_text(cid, part_id):
    if cid == 1:
        text = generate_msg(CPUs[part_id])     
    if cid == 2:
        text = generate_msg(MBs[part_id])
    if cid == 3:
        text = generate_msg(VCs[part_id])
    if cid == 4:
        text = generate_msg(RAMs[part_id])
    if cid == 5:
        text = generate_msg(PSs[part_id])        
             
    return text

def generate_kb():
    pass

def get_next_part_id(key, d):
    pos = 0
    for i in d:
        if i == key:
            listForm = list(d.keys())
            return listForm[pos+1]
        pos += 1

def get_prev_part_id(key, d):
    pos = 0
    for i in d:
        if i == key:
            listForm = list(d.keys())
            return listForm[pos-1]
        pos += 1

def get_last_id_for_categ(d):
    return list(d.keys())[-1]

def get_all_cost(tupl):
    result = 0
    for part in tupl:
        p_id = part[0]
        if p_id in CPUs:
            result += part[1]*CPUs[p_id][4]
        if p_id in MBs:
            result += part[1]*MBs[p_id][4]
        if p_id in VCs:
            result += part[1]*VCs[p_id][4]
        if p_id in RAMs:
            result += part[1]*RAMs[p_id][4]
        if p_id in PSs:
            result += part[1]*PSs[p_id][4]    
        
    return result
    
    