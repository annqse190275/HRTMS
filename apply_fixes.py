import re

def main():
    file_path = r'd:\study\SUMMER2026\SWP391\HRTMS\src\pres\index.html'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace swimlane-matrix with branching-flow-svg container
    swimlane_pattern = r'<div class="space-y-3" id="swimlane-matrix">.*?(?=</div>\s*</div>\s*<!-- Right: Business)'
    svg_container_html = '''
<div class="relative w-full h-[600px] overflow-hidden bg-slate-950 rounded-2xl border border-slate-800 shadow-inner" id="svg-container">
    <svg id="branching-flow-svg" class="w-full h-full absolute inset-0 z-10">
        <defs>
            <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
                <feGaussianBlur stdDeviation="3" result="blur" />
                <feComposite in="SourceGraphic" in2="blur" operator="over" />
            </filter>
            <!-- Markers -->
            <marker id="arrow-emerald" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0 L0,6 L6,3 z" fill="#10B981" /></marker>
            <marker id="arrow-indigo" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0 L0,6 L6,3 z" fill="#6366f1" /></marker>
            <marker id="arrow-amber" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0 L0,6 L6,3 z" fill="#F59E0B" /></marker>
            <marker id="arrow-purple" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0 L0,6 L6,3 z" fill="#a855f7" /></marker>
            <marker id="arrow-pink" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0 L0,6 L6,3 z" fill="#ec4899" /></marker>
            <marker id="arrow-slate" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0 L0,6 L6,3 z" fill="#1e293b" /></marker>
            <marker id="arrow-red" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0 L0,6 L6,3 z" fill="#DC2626" /></marker>
            <marker id="arrow-gray" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0 L0,6 L6,3 z" fill="#475569" /></marker>
        </defs>
        <g id="svg-paths"></g>
        <g id="svg-nodes"></g>
    </svg>
    <!-- Phase 5 Live Simulation Canvas -->
    <div id="live-race-container" class="absolute inset-0 z-20 bg-slate-900 flex flex-col hidden p-4">
        <div class="flex justify-between items-center mb-4 border-b border-slate-800 pb-2">
            <h4 class="text-emerald-400 font-bold uppercase text-xs flex items-center gap-2"><i data-lucide="play-circle" class="w-4 h-4"></i> Live Racing Simulation</h4>
            <button onclick="toggleLiveRace()" class="text-xs text-slate-400 hover:text-white bg-slate-800 px-2 py-1 rounded">Đóng</button>
        </div>
        <canvas id="live-race-canvas" class="w-full flex-1 rounded-xl bg-[#0f172a]"></canvas>
    </div>
    <style>
        .path-animated {
            stroke-dasharray: 8;
            animation: dash 1.5s linear infinite;
        }
        @keyframes dash {
            to { stroke-dashoffset: -16; }
        }
        .node-hover {
            transition: all 0.3s ease;
        }
        .node-hover:hover {
            filter: brightness(1.2);
            cursor: pointer;
        }
        .node-dimmed {
            opacity: 0.2;
            filter: grayscale(100%);
            pointer-events: none;
        }
    </style>
</div>
'''
    content = re.sub(swimlane_pattern, svg_container_html, content, flags=re.DOTALL)

    # 2. Inject JS Logic
    script_start = content.find('const THEME = {')
    script_logic = """
        const GLOBAL_SIM_STATE = {
            activeErrors: []
        };
        
        let liveRaceInterval = null;
        let horses = [];
        
        function logToConsole(type, message) {
            const terminal = document.getElementById('sim-terminal');
            const logLine = document.createElement('p');
            if (type === 'INFO') {
                logLine.className = "text-emerald-400 font-mono";
            } else if (type === 'WARNING') {
                logLine.className = "text-amber-400 font-mono";
            } else if (type === 'URGENT' || type === 'ERROR') {
                logLine.className = "text-rose-500 font-mono font-bold";
            } else {
                logLine.className = "text-blue-400 font-mono";
            }
            logLine.innerText = `[${type}] ${message}`;
            terminal.appendChild(logLine);
            terminal.scrollTop = terminal.scrollHeight;
        }

        function toggleErrorOnCheckpoint(errorId, phaseId, node) {
            // Special popups/interactions
            if (errorId === 'horse_reg_rejected' && !GLOBAL_SIM_STATE.activeErrors.includes(errorId)) {
                const reason = prompt("Lỗi Duyệt Hồ Sơ: Nhập lý do từ chối (>= 10 ký tự):");
                if (!reason || reason.length < 10) {
                    alert("Lý do quá ngắn. Đã hủy thao tác bẻ luồng.");
                    return;
                }
                logToConsole("WARNING", `Duyệt hồ sơ ngựa bị từ chối. Lý do: ${reason}`);
            }
            
            const idx = GLOBAL_SIM_STATE.activeErrors.indexOf(errorId);
            if (idx > -1) {
                GLOBAL_SIM_STATE.activeErrors.splice(idx, 1);
                logToConsole("INFO", `Đã gỡ bỏ nhánh ngoại lệ: ${errorId}. Khôi phục Happy Path.`);
            } else {
                GLOBAL_SIM_STATE.activeErrors.push(errorId);
                
                // Trigger specific console logs based on BA rules
                if (errorId === 'owner_missed_confirmation') {
                    logToConsole("URGENT", "Chủ ngựa rút lui đột xuất/quá hạn 24h. Trạng thái Cancelled. Vị trí cổng xuất phát đổi thành Vacant.");
                } else if (errorId === 'coi_conflict_detected') {
                    logToConsole("URGENT", "Trọng tài có quan hệ trực hệ với Owner. Bị chặn phân công do xung đột lợi ích!");
                } else if (['identity_mismatch', 'horse_health_unfit', 'jockey_independence_conflict'].includes(errorId)) {
                    logToConsole("URGENT", `Phát hiện lỗi ${errorId}. Khẩn cấp truất quyền thi đấu (DISQ). Hoàn trả toàn bộ 200 điểm dự đoán ảo (Refund virtual points) cho khán giả.`);
                } else if (errorId === 'protest_approved') {
                    logToConsole("WARNING", "Chấp thuận khiếu nại (Protest). Quyết định: Phạt Place Behind. Bảng xếp hạng sơ bộ đã được cập nhật.");
                } else if (errorId === 'transaction_rollback') {
                    logToConsole("ERROR", "Lỗi Backend Database: Rollback toàn bộ ACID Transaction. Cuộc đua bị giam ở trạng thái Unofficial. Đóng băng trả thưởng.");
                } else {
                    logToConsole("WARNING", `Kích hoạt ngoại lệ: ${errorId}`);
                }
            }
            
            renderBranchingFlow(phaseId);
        }
        
        function isNodeAffectedByError(nodeId, phaseId) {
            const errs = GLOBAL_SIM_STATE.activeErrors;
            // Phase 2 error cascades
            if (errs.includes('horse_reg_rejected') && phaseId >= 3) return true;
            // Phase 3 error cascades
            if (errs.includes('owner_missed_confirmation') && phaseId >= 4 && !nodeId.includes('err')) return true;
            if (errs.includes('coi_conflict_detected') && phaseId === 5 && nodeId === '5-1') return true; // Cấm Live start
            // Phase 4 error cascades (DISQ)
            if ((errs.includes('identity_mismatch') || errs.includes('horse_health_unfit') || errs.includes('jockey_independence_conflict')) && phaseId >= 5) {
                if (!nodeId.includes('err') && !nodeId.includes('disq')) return true; 
            }
            // Phase 6 rollback
            if (errs.includes('transaction_rollback') && phaseId === 6 && nodeId === '6-2') return true; // Đóng băng chia thưởng
            
            return false;
        }

        function toggleLiveRace() {
            const container = document.getElementById('live-race-container');
            const svg = document.getElementById('branching-flow-svg');
            if (container.classList.contains('hidden')) {
                container.classList.remove('hidden');
                svg.classList.add('hidden');
                startLiveSimulation();
            } else {
                container.classList.add('hidden');
                svg.classList.remove('hidden');
                stopLiveSimulation();
            }
        }

        function startLiveSimulation() {
            const canvas = document.getElementById('live-race-canvas');
            const ctx = canvas.getContext('2d');
            // Resize canvas to fit container
            canvas.width = canvas.parentElement.clientWidth - 32; // padding
            canvas.height = canvas.parentElement.clientHeight - 60; // header padding

            const errs = GLOBAL_SIM_STATE.activeErrors;
            const hasDisq = errs.includes('horse_health_unfit') || errs.includes('coi_conflict_detected') || errs.includes('identity_mismatch') || errs.includes('jockey_independence_conflict');

            horses = [];
            for (let i = 0; i < 10; i++) {
                horses.push({
                    id: i + 1,
                    x: 10,
                    y: 20 + i * (canvas.height / 10),
                    speed: (Math.random() * 2) + 1,
                    isDisqualified: (i === 3 && hasDisq) // Make horse 4 the disqualified one if error is active
                });
            }

            if (liveRaceInterval) clearInterval(liveRaceInterval);
            
            liveRaceInterval = setInterval(() => {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                
                // Draw finish line
                ctx.strokeStyle = '#D4AF37';
                ctx.setLineDash([10, 10]);
                ctx.beginPath();
                ctx.moveTo(canvas.width - 50, 0);
                ctx.lineTo(canvas.width - 50, canvas.height);
                ctx.stroke();
                ctx.setLineDash([]);

                horses.forEach(h => {
                    // Update position
                    if (!h.isDisqualified && h.x < canvas.width - 60) {
                        h.x += (Math.random() * 3) + 1; // Random speed burst
                    }

                    // Draw lane
                    ctx.fillStyle = '#1e293b';
                    ctx.fillRect(0, h.y, canvas.width, 20);

                    // Draw horse chip
                    ctx.fillStyle = h.isDisqualified ? '#dc2626' : '#10b981';
                    ctx.beginPath();
                    ctx.arc(h.x + 10, h.y + 10, 8, 0, Math.PI * 2);
                    ctx.fill();
                    
                    // Draw number
                    ctx.fillStyle = '#ffffff';
                    ctx.font = '10px Arial';
                    ctx.textAlign = 'center';
                    ctx.fillText(h.id, h.x + 10, h.y + 13);

                    if (h.isDisqualified) {
                        ctx.fillStyle = '#fca5a5';
                        ctx.fillText('DISQUALIFIED', h.x + 60, h.y + 13);
                    }
                });
            }, 100);
        }

        function stopLiveSimulation() {
            if (liveRaceInterval) clearInterval(liveRaceInterval);
        }

        function renderBranchingFlow(phaseId) {
            const data = phaseData[phaseId];
            if (!data || !data.flowNodes) return;
            
            const pathsGroup = document.getElementById('svg-paths');
            const nodesGroup = document.getElementById('svg-nodes');
            pathsGroup.innerHTML = '';
            nodesGroup.innerHTML = '';
            
            const nodeMap = {};
            data.flowNodes.forEach(n => { nodeMap[n.id] = n; });
            
            // Draw connections
            data.flowConnections.forEach(conn => {
                const src = nodeMap[conn.src];
                const dst = nodeMap[conn.dst];
                if (!src || !dst) return;
                
                if (conn.isErrorBranch && !GLOBAL_SIM_STATE.activeErrors.includes(conn.errorId)) return;
                
                let strokeColor = conn.isErrorBranch ? '#DC2626' : '#6366f1'; 
                let marker = conn.isErrorBranch ? 'url(#arrow-red)' : 'url(#arrow-indigo)';
                let isDimmed = false;
                
                // If happy path but error is active, dim it
                if (!conn.isErrorBranch && conn.errorId && GLOBAL_SIM_STATE.activeErrors.includes(conn.errorId)) {
                    strokeColor = '#475569';
                    marker = 'url(#arrow-gray)';
                    isDimmed = true;
                }
                if (isNodeAffectedByError(conn.dst, phaseId) || isNodeAffectedByError(conn.src, phaseId)) {
                    strokeColor = '#475569';
                    marker = 'url(#arrow-gray)';
                    isDimmed = true;
                }
                
                const sx = src.x + (src.w || 150) / 2;
                const sy = src.y + (src.h || 44) / 2;
                const dx = dst.x + (dst.w || 150) / 2;
                const dy = dst.y + (dst.h || 44) / 2;
                
                const pathStr = `M ${sx},${sy} C ${(sx+dx)/2},${sy} ${(sx+dx)/2},${dy} ${dx},${dy}`;
                const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
                path.setAttribute("d", pathStr);
                path.setAttribute("fill", "none");
                path.setAttribute("stroke", strokeColor);
                path.setAttribute("stroke-width", "2.5");
                path.setAttribute("marker-end", marker);
                if (conn.isErrorBranch) path.setAttribute("class", "path-animated");
                if (isDimmed) path.setAttribute("opacity", "0.2");
                
                pathsGroup.appendChild(path);
            });
            
            // Draw nodes
            data.flowNodes.forEach(n => {
                const isErrorNode = n.type === 'error';
                const isCheckpoint = n.type === 'checkpoint';
                
                if (isErrorNode && !GLOBAL_SIM_STATE.activeErrors.includes(n.errorId)) return;
                
                let isDimmed = isNodeAffectedByError(n.id, phaseId);
                if (n.errorId && !isErrorNode && !isCheckpoint && GLOBAL_SIM_STATE.activeErrors.includes(n.errorId)) {
                    isDimmed = true;
                }
                
                let fill = '#0f172a';
                let stroke = '#475569';
                let textColor = '#e2e8f0';
                
                // Colors mapped 1:1 with BA rules
                if (n.actor === 'admin') stroke = '#6366f1'; // Indigo
                if (n.actor === 'owner') stroke = '#10B981'; // Emerald
                if (n.actor === 'jockey') stroke = '#F59E0B'; // Amber
                if (n.actor === 'referee') stroke = '#a855f7'; // Purple
                if (n.actor === 'spectator') stroke = '#ec4899'; // Pink
                if (n.actor === 'system') stroke = '#1e293b'; // Slate-800
                
                if (isErrorNode) {
                    fill = '#450a0a'; stroke = '#dc2626'; textColor = '#fca5a5';
                } else if (isCheckpoint) {
                    stroke = '#f59e0b';
                    pathClass = "path-animated"; // Not applied to rect, but we can set stroke-dasharray
                }
                
                const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
                g.setAttribute("class", isDimmed ? "node-dimmed" : "node-hover");
                
                if (isCheckpoint) {
                    g.onclick = () => toggleErrorOnCheckpoint(n.errorId, phaseId, n);
                }
                
                if (n.id === '5-live-btn') {
                    g.onclick = () => toggleLiveRace();
                }
                
                const w = n.w || 150;
                const h = n.h || 44;
                
                const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
                rect.setAttribute("x", n.x);
                rect.setAttribute("y", n.y);
                rect.setAttribute("width", w);
                rect.setAttribute("height", h);
                rect.setAttribute("rx", n.actor === 'system' ? "22" : "8"); // Circle/pill for system
                rect.setAttribute("fill", fill);
                rect.setAttribute("stroke", stroke);
                rect.setAttribute("stroke-width", "2");
                if (isCheckpoint) rect.setAttribute("stroke-dasharray", "4");
                g.appendChild(rect);
                
                // Label lines (split by |)
                const lines = n.label.split('|');
                lines.forEach((line, i) => {
                    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
                    text.setAttribute("x", n.x + w/2);
                    text.setAttribute("y", n.y + h/2 + (lines.length > 1 ? (i===0 ? -4 : 10) : 4));
                    text.setAttribute("fill", textColor);
                    text.setAttribute("font-size", i===0 && lines.length > 1 ? "11" : "10");
                    text.setAttribute("font-weight", isCheckpoint || (i===0 && lines.length > 1) ? "bold" : "normal");
                    text.setAttribute("text-anchor", "middle");
                    text.innerHTML = line;
                    g.appendChild(text);
                });
                
                if (isCheckpoint) {
                    const icon = document.createElementNS("http://www.w3.org/2000/svg", "text");
                    icon.setAttribute("x", n.x + w - 18);
                    icon.setAttribute("y", n.y + 16);
                    icon.setAttribute("font-size", "12");
                    icon.innerHTML = "⚙️";
                    g.appendChild(icon);
                }
                
                nodesGroup.appendChild(g);
            });
        }
"""
    content = content[:script_start] + script_logic + content[script_start:]

    # 3. Add flowData properly to PhaseData
    # Let's dynamically insert flowNodes & flowConnections for Phase 1 to 6
    flow_data_map = {
        '1': '''
                flowNodes: [
                    { id: '1-1', label: 'Tạo giải & Cấu hình', x: 20, y: 50, actor: 'admin' },
                    { id: '1-2', label: 'Cấu hình Vòng Đua', x: 220, y: 50, actor: 'admin' },
                    { id: '1-3', label: 'Phân quỹ Purse', x: 420, y: 50, actor: 'admin' },
                    { id: '1-4', label: 'Spectator Xem Giải', x: 420, y: 150, actor: 'spectator' }
                ],
                flowConnections: [
                    { src: '1-1', dst: '1-2' },
                    { src: '1-2', dst: '1-3' },
                    { src: '1-3', dst: '1-4' }
                ],''',
        '2': '''
                flowNodes: [
                    { id: '2-1', label: 'Owner Tạo Hồ Sơ', x: 20, y: 20, actor: 'owner' },
                    { id: '2-5', label: 'Duyệt Hồ Sơ|Kiểm Duyệt', x: 220, y: 20, actor: 'admin', type: 'checkpoint', errorId: 'horse_reg_rejected' },
                    { id: '2-err', label: 'Từ chối (Lý do >=10 kí tự)|Auto-reject', x: 220, y: 120, actor: 'admin', type: 'error', errorId: 'horse_reg_rejected' },
                    { id: '2-3', label: 'Mời Jockey', x: 420, y: 20, actor: 'owner' },
                    { id: '2-4', label: 'Jockey Chấp Nhận', x: 420, y: 120, actor: 'jockey' },
                    { id: '2-6', label: 'Ghép Cặp Thành Công', x: 620, y: 70, actor: 'owner' }
                ],
                flowConnections: [
                    { src: '2-1', dst: '2-5' },
                    { src: '2-5', dst: '2-3', errorId: 'horse_reg_rejected' },
                    { src: '2-5', dst: '2-err', isErrorBranch: true, errorId: 'horse_reg_rejected' },
                    { src: '2-4', dst: '2-3' },
                    { src: '2-3', dst: '2-6' }
                ],''',
        '3': '''
                flowNodes: [
                    { id: '3-1', label: 'Phân bổ Ngựa', x: 20, y: 20, actor: 'admin' },
                    { id: '3-2', label: 'Bốc thăm Post Position', x: 220, y: 20, actor: 'admin' },
                    { id: '3-3', label: 'Xác Nhận Tham Gia|Rút lui', x: 220, y: 100, actor: 'owner', type: 'checkpoint', errorId: 'owner_missed_confirmation' },
                    { id: '3-err1', label: 'Cancelled / Vacant|Rút lui đột xuất', x: 220, y: 180, actor: 'system', type: 'error', errorId: 'owner_missed_confirmation' },
                    { id: '3-5', label: 'Phân công Trọng Tài|COI Check', x: 420, y: 20, actor: 'admin', type: 'checkpoint', errorId: 'coi_conflict_detected' },
                    { id: '3-err2', label: 'COI Conflict Detected|Cấm Phân Công', x: 420, y: 100, actor: 'system', type: 'error', errorId: 'coi_conflict_detected' },
                    { id: '3-4', label: 'Mở Cổng Dự Đoán', x: 620, y: 20, actor: 'admin' }
                ],
                flowConnections: [
                    { src: '3-1', dst: '3-2' },
                    { src: '3-2', dst: '3-5' },
                    { src: '3-2', dst: '3-3' },
                    { src: '3-3', dst: '3-err1', isErrorBranch: true, errorId: 'owner_missed_confirmation' },
                    { src: '3-5', dst: '3-err2', isErrorBranch: true, errorId: 'coi_conflict_detected' },
                    { src: '3-5', dst: '3-4', errorId: 'coi_conflict_detected' }
                ],''',
        '4': '''
                flowNodes: [
                    { id: '4-1', label: 'Xác Minh Danh Tính|Kiểm Duyệt', x: 20, y: 20, actor: 'referee', type: 'checkpoint', errorId: 'identity_mismatch' },
                    { id: '4-2', label: 'Kiểm Tra Sức Khỏe|Thủ Công', x: 220, y: 20, actor: 'referee', type: 'checkpoint', errorId: 'horse_health_unfit' },
                    { id: '4-3', label: 'Jockey Independence|Kiểm Duyệt', x: 420, y: 20, actor: 'referee', type: 'checkpoint', errorId: 'jockey_independence_conflict' },
                    { id: '4-5-DISQ', label: '4.5-DISQ|Refund Points', x: 220, y: 120, actor: 'system', type: 'error', errorId: 'identity_mismatch', w: 180 },
                    { id: '4-4', label: 'Hoàn Tất Chuẩn Bị', x: 620, y: 20, actor: 'referee' }
                ],
                flowConnections: [
                    { src: '4-1', dst: '4-2', errorId: 'identity_mismatch' },
                    { src: '4-1', dst: '4-5-DISQ', isErrorBranch: true, errorId: 'identity_mismatch' },
                    { src: '4-2', dst: '4-3', errorId: 'horse_health_unfit' },
                    { src: '4-2', dst: '4-5-DISQ', isErrorBranch: true, errorId: 'horse_health_unfit' },
                    { src: '4-3', dst: '4-4', errorId: 'jockey_independence_conflict' },
                    { src: '4-3', dst: '4-5-DISQ', isErrorBranch: true, errorId: 'jockey_independence_conflict' }
                ],''',
        '5': '''
                flowNodes: [
                    { id: '5-1', label: 'Bấm LIVE Start', x: 20, y: 20, actor: 'referee' },
                    { id: '5-live-btn', label: '▶ XEM MÔ PHỎNG LÀN CHẠY', x: 20, y: 120, actor: 'spectator', w: 180, h: 40 },
                    { id: '5-2', label: 'Khóa Cổng Cược', x: 220, y: 20, actor: 'system' },
                    { id: '5-5', label: 'Xử Lý Protest|Khiếu nại', x: 420, y: 20, actor: 'referee', type: 'checkpoint', errorId: 'protest_approved' },
                    { id: '5-err', label: 'PlaceBehind/DISQ', x: 420, y: 120, actor: 'referee', type: 'error', errorId: 'protest_approved' },
                    { id: '5-6', label: 'Unofficial Result', x: 620, y: 20, actor: 'referee' }
                ],
                flowConnections: [
                    { src: '5-1', dst: '5-2' },
                    { src: '5-2', dst: '5-5' },
                    { src: '5-5', dst: '5-6', errorId: 'protest_approved' },
                    { src: '5-5', dst: '5-err', isErrorBranch: true, errorId: 'protest_approved' },
                    { src: '5-err', dst: '5-6', isErrorBranch: true, errorId: 'protest_approved' }
                ],''',
        '6': '''
                flowNodes: [
                    { id: '6-1', label: 'Chuyển Official', x: 20, y: 20, actor: 'admin', type: 'checkpoint', errorId: 'transaction_rollback' },
                    { id: '6-err', label: 'Rollback ACID Trans|Giam Unofficial', x: 20, y: 120, actor: 'system', type: 'error', errorId: 'transaction_rollback' },
                    { id: '6-2', label: 'Chia Thưởng', x: 220, y: 20, actor: 'admin' },
                    { id: '6-3', label: 'Cộng Điểm Spectator', x: 420, y: 20, actor: 'system' },
                    { id: '6-4', label: 'Audit Log Khóa Cứng', x: 620, y: 20, actor: 'system' }
                ],
                flowConnections: [
                    { src: '6-1', dst: '6-2', errorId: 'transaction_rollback' },
                    { src: '6-1', dst: '6-err', isErrorBranch: true, errorId: 'transaction_rollback' },
                    { src: '6-2', dst: '6-3' },
                    { src: '6-3', dst: '6-4' }
                ],'''
    }

    for phase_id in ['1', '2', '3', '4', '5', '6']:
        pattern = f'({phase_id}: {{\n\\s*title:.*?actions: {{)'
        content = re.sub(pattern, flow_data_map[phase_id] + r'\1', content)

    # 4. Integrate with selectPhase
    content = content.replace('// Simulate drawing lanes', 'renderBranchingFlow(phaseId);')
    # Prevent old UI list from breaking by wrapping in try/catch or just executing renderBranchingFlow
    content = content.replace('document.getElementById(`swim-${role}-actions`).innerHTML = "";', 'const el = document.getElementById(`swim-${role}-actions`); if(el) el.innerHTML = "";')
    content = content.replace('// Populate Swimlane lists', 'renderBranchingFlow(phaseId);')

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    main()
