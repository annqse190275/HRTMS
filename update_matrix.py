import sys

with open('D:/study/SUMMER2026/SWP391/HRTMS/src/pres/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the table wrapper
old_wrapper = '<div class="w-full overflow-x-auto rounded-xl border border-slate-800">'
new_wrapper = '<div class="w-full max-h-[600px] overflow-auto border border-slate-800 rounded-xl scrollbar-thin">'
content = content.replace(old_wrapper, new_wrapper)

# 2. Update the thead to have sticky phase headers
start_thead = content.find('<thead>')
end_thead = content.find('</thead>') + len('</thead>')
thead_content = content[start_thead:end_thead]

# 3. Modify Top-Left Corner
top_left_th_old = 'class="p-4 border-r border-slate-800 w-[12%] bg-slate-950/90 sticky left-0 z-10"'
top_left_th_new = 'class="p-4 border-r border-slate-800 w-[12%] sticky top-0 left-0 z-40 bg-slate-900"'
thead_content = thead_content.replace(top_left_th_old, top_left_th_new)

# Modify other th elements in thead
other_th_old = 'class="p-4 border-r border-slate-800 w-[14%]"'
other_th_new = 'class="p-4 border-r border-slate-800 w-[14%] sticky top-0 z-30 bg-slate-900"'
thead_content = thead_content.replace(other_th_old, other_th_new)

spec_th_old = 'class="p-4 w-[18%]"'
spec_th_new = 'class="p-4 w-[18%] sticky top-0 z-30 bg-slate-900"'
thead_content = thead_content.replace(spec_th_old, spec_th_new)

content = content[:start_thead] + thead_content + content[end_thead:]

# 4. Modify sticky left for tbody tds (Giai đoạn column)
td_left_old = 'class="p-4 font-bold border-r border-slate-800 bg-slate-950/40 sticky left-0 z-10"'
td_left_new = 'class="p-4 font-bold border-r border-slate-800 sticky left-0 z-20 bg-slate-950"'
content = content.replace(td_left_old, td_left_new)

with open('D:/study/SUMMER2026/SWP391/HRTMS/src/pres/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated Matrix mode styling.')
