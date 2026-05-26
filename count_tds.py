with open('D:/study/SUMMER2026/SWP391/HRTMS/src/pres/index.html', 'r', encoding='utf-8') as f:
    c = f.read()
count = c.count('class="p-4 font-bold border-r border-slate-800 sticky left-0 z-20 bg-slate-950"')
print(f'Number of updated tds: {count}')
