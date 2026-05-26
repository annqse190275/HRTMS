import sys
import re

with open('D:/study/SUMMER2026/SWP391/HRTMS/src/pres/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

start_loop = content.find('// 1. Draw Visual Background Swimlanes')
end_loop = content.find('// Map nodes')

if start_loop != -1 and end_loop != -1:
    loop_content = content[start_loop:end_loop]
    
    new_loop_content = re.sub(
        r'// Lane Label.*?nodesGroup\.appendChild\(label\);',
        '',
        loop_content,
        flags=re.DOTALL
    )

    insert_clear = '''const stickyCol = document.getElementById('sticky-actors-col');
            if (stickyCol) stickyCol.innerHTML = '';
            
            // 1. Draw Visual Background Swimlanes'''
    new_loop_content = new_loop_content.replace('// 1. Draw Visual Background Swimlanes', insert_clear)

    append_html = '''
                const laneDiv = document.createElement('div');
                laneDiv.className = 'flex items-center justify-center border-b border-slate-800 text-[9px] sm:text-[10px] font-extrabold uppercase tracking-wider text-center p-2';
                laneDiv.style.height = (lane.yMax - lane.yMin) + 'px';
                laneDiv.style.color = lane.textColor;
                laneDiv.style.opacity = '0.7';
                laneDiv.innerHTML = lane.name;
                if (stickyCol) stickyCol.appendChild(laneDiv);
'''
    new_loop_content = new_loop_content.replace('pathsGroup.appendChild(rect);', 'pathsGroup.appendChild(rect);' + append_html)

    content = content[:start_loop] + new_loop_content + content[end_loop:]

    with open('D:/study/SUMMER2026/SWP391/HRTMS/src/pres/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('JS Layout updated.')
else:
    print('Could not find JS block')
