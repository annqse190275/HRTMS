import sys

with open('D:/study/SUMMER2026/SWP391/HRTMS/src/pres/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. We want to move 'Phases Horizontal Timeline' into the left column.
start_phase = content.find('<!-- Phases Horizontal Timeline (6 stages) -->')
end_phase = content.find('<!-- GLOBAL SIMULATION STATE wrapper with absolute overlay panel inside -->')
if start_phase != -1 and end_phase != -1:
    phase_block = content[start_phase:end_phase].strip()
    phase_block = phase_block.replace('<div class="flex flex-col gap-2">', '<div class="grid grid-cols-3 md:grid-cols-6 gap-2">')
    content = content[:start_phase] + content[end_phase:]
else:
    print("Could not find Phase block")
    sys.exit(1)

# 2. Change the left column wrapper
old_left_col = '<div class="col-span-8 bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4">'
new_left_col = f'''<div class="col-span-12 lg:col-span-7 flex flex-col gap-4">
                            {phase_block}
                            <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-4 flex-1">
'''
if old_left_col in content:
    content = content.replace(old_left_col, new_left_col)
else:
    print("Could not find left column wrapper")

# Close the extra div for the left column
old_left_end = '''</div>
                        </div>

                        <!-- Right: Business Sandbox Simulator Terminal Panel -->'''
new_left_end = '''</div>
                            </div>
                        </div>

                        <!-- Right: Business Sandbox Simulator Terminal Panel -->'''
if old_left_end in content:
    content = content.replace(old_left_end, new_left_end)
elif '''</div>\n\n                        <!-- Right: Business Sandbox Simulator Terminal Panel -->''' in content:
    content = content.replace('''</div>\n\n                        <!-- Right: Business Sandbox Simulator Terminal Panel -->''', '''</div>\n                            </div>\n                        </div>\n\n                        <!-- Right: Business Sandbox Simulator Terminal Panel -->''')

# 3. Change Right column wrapper
old_right_col = '<div class="col-span-4 sticky top-6 flex flex-col gap-4">'
new_right_col = '<div class="col-span-12 lg:col-span-5 flex flex-col gap-4 h-[720px] overflow-y-auto">'
content = content.replace(old_right_col, new_right_col)

# 4. Modify the SVG container to add sticky actors column
old_svg_wrapper = '''<div class="relative w-full h-[800px] overflow-hidden bg-slate-950 rounded-2xl border border-slate-800 shadow-inner" id="svg-container">
    <svg id="branching-flow-svg" class="w-full h-full absolute inset-0 z-10">'''
new_svg_wrapper = '''<div class="relative w-full bg-slate-950 rounded-2xl border border-slate-800 shadow-inner flex" style="min-h: 660px;">
    <div class="w-32 sm:w-48 sticky left-0 z-20 bg-slate-950 border-r border-slate-800 flex flex-col shrink-0" id="sticky-actors-col">
        <!-- Sticky actors column populated by JS -->
    </div>
    <div class="w-full overflow-x-auto scrollbar-thin">
        <div class="relative min-w-[1000px] h-[660px]" id="svg-container">
            <svg id="branching-flow-svg" class="w-full h-full absolute inset-0 z-10">'''
if old_svg_wrapper in content:
    content = content.replace(old_svg_wrapper, new_svg_wrapper)
else:
    print("Could not find SVG wrapper")

old_svg_end = '''</style>
</div>'''
new_svg_end = '''</style>
        </div>
    </div>
</div>'''
if old_svg_end in content:
    content = content.replace(old_svg_end, new_svg_end)

# 5. Move Actor Actions Details to the BOTTOM ZONE
start_details = content.find('<!-- Actor Actions Details -->')
end_details = content.find('</section>', start_details)

if start_details != -1 and end_details != -1:
    details_block = content[start_details:end_details].strip()
    old_details_div = '<div class="bg-slate-900 border border-slate-800 rounded-2xl p-6 mt-6">'
    new_details_div = '''<div class="col-span-12 w-full mt-4">
                        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6">'''
    details_block = details_block.replace(old_details_div, new_details_div)
    details_block += '\n</div>'
    
    # Remove from old location
    content = content[:start_details] + content[end_details:]
    
    # Add to bottom zone
    end_details_new = content.find('</section>', start_details)
    content = content[:end_details_new] + details_block + '\n            ' + content[end_details_new:]

# Write back
with open('D:/study/SUMMER2026/SWP391/HRTMS/src/pres/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("HTML DOM Re-structured successfully.")
