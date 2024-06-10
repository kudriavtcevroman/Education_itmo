import names, numpy as np
lst_names = np.array([''.join(names.get_first_name()) for _ in range(100)])
a_m_volume = 'ABCDEFGHIJKLM'
lst_names_a_m = []
lst_names_m_z = []
for i in range(len(lst_names)):
    if lst_names[i][0] in a_m_volume:
        lst_names_a_m.append(lst_names[i])
    else:
        lst_names_m_z.append(lst_names[i])
print(lst_names_a_m)
print(lst_names_m_z)