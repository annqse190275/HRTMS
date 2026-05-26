import sys

with open('D:/study/SUMMER2026/SWP391/HRTMS/src/pres/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_str = '''                    <!-- Actor Actions Details -->
                    <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 mt-6">'''
new_str = '''                    <!-- Actor Actions Details -->
                    <div class="col-span-12 w-full mt-4">
                        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6">'''

if old_str in content:
    content = content.replace(old_str, new_str)
    
    end_pattern = '''                        </div>
                    </div>
                </div>

                <!-- COMPLETE MA TRẬN SWIMLANE VIEW (Subtab 2 - Built on hrtms_swimlane_workflow.html) -->'''
    new_end_pattern = '''                        </div>
                        </div>
                    </div>
                </div>

                <!-- COMPLETE MA TRẬN SWIMLANE VIEW (Subtab 2 - Built on hrtms_swimlane_workflow.html) -->'''
    content = content.replace(end_pattern, new_end_pattern)

    with open('D:/study/SUMMER2026/SWP391/HRTMS/src/pres/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Fixed Actor Actions Details wrapper.')
else:
    print('Pattern not found')
