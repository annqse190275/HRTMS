import re

def update_index():
    file_path = r'd:\study\SUMMER2026\SWP391\HRTMS\src\pres\index.html'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update MODULE_CAT_MAP
    new_cat_map = """const MODULE_CAT_MAP = {
            A: 'platform', B: 'tournament', C: 'registration', D: 'registration',
            E: 'tournament', F: 'tournament', G: 'racing', H: 'racing', I: 'racing',
            J: 'results', K: 'results', L: 'results', M: 'prediction', N: 'prediction',
            O: 'support', P: 'support', Q: 'platform'
        };"""
    content = re.sub(r'const MODULE_CAT_MAP = \{[\s\S]*?\};', new_cat_map, content)

    # 2. Update IN_SCOPE_MODULES
    new_in_scope = """const IN_SCOPE_MODULES = [
            { id: 'A', title: 'Quản Lý Tài Khoản và Phân Quyền', icon: 'shield-check', desc: 'Horse Owner, Jockey, Race Referee, Spectator tự đăng ký. Admin quản lý tài khoản theo role. Xác thực username/password. Phân quyền RBAC. Tuân thủ OWASP Top 10 và ISO 27001.' },
            { id: 'B', title: 'Quản Lý Giải Đấu', icon: 'trophy', desc: 'Admin tạo giải (tên, thời gian, quy mô, loại hình đua). Cấu hình cấu trúc vòng đua (vòng loại → bán kết → chung kết). Quản lý và cập nhật thông tin giải sau khi tạo.' },
            { id: 'C', title: 'Đăng Ký Ngựa Thi Đấu và Duyệt Hồ Sơ', icon: 'file-plus-2', desc: 'Horse Owner đăng ký ngựa (tên, tuổi, giới tính, huyết thống, trọng lượng, đặc điểm). Admin duyệt/từ chối kèm lý do. F1: bước duyệt không kiểm tra chứng chỉ Jockey. F3: sức khỏe ngựa ghi nhận thủ công.' },
            { id: 'D', title: 'Quản Lý Nài ngựa (Jockey)', icon: 'user-plus', desc: 'Jockey đăng ký tài khoản với chứng chỉ hành nghề. Horse Owner tìm kiếm, gửi lời mời. Jockey xác nhận/từ chối. Horse Owner chốt ghép cặp ngựa–Jockey chính thức.' },
            { id: 'E', title: 'Lập Lịch Thi Đấu, Bốc Thăm và Sắp Xếp Cuộc Đua', icon: 'calendar-days', desc: 'Admin phân bổ ngựa đã duyệt, xác định ngày giờ, bốc thăm Post Position ngẫu nhiên công khai. Sinh lịch tự động. Horse Owner xác nhận tham gia để đưa ngựa vào danh sách xuất phát.' },
            { id: 'F', title: 'Phân Công Trọng Tài và Referee COI Check', icon: 'user-cog', desc: 'Admin phân công Lead + Assistant Referees. Referee COI Check: không có quan hệ gia đình trực hệ với Horse Owner. Thông báo phân công. Lưu trữ lịch sử ≥5 ngày trước đua.' },
            { id: 'G', title: 'Kiểm Tra Trước Thi Đấu (Pre-race Preparation)', icon: 'stethoscope', desc: 'Race Referee xác minh danh tính ngựa, ghi nhận sức khỏe thủ công. Jockey Independence Check: chứng chỉ hợp lệ, không quan hệ gia đình với Horse Owner trong cùng cuộc đua. Tách biệt khỏi bước duyệt hồ sơ.' },
            { id: 'H', title: 'Theo Dõi Diễn Biến Cuộc Đua và Xử Lý Vi Phạm', icon: 'eye', desc: 'Race Referee quản lý trạng thái: Upcoming → Live → Unofficial. Tự động khóa cổng dự đoán khi Live. Ghi nhận vi phạm bằng dropdown mã lỗi.' },
            { id: 'I', title: 'Xử Lý Vi Phạm và Khiếu Nại (Protest Handling)', icon: 'scale', desc: 'Race Referee tiếp nhận khiếu nại từ Horse Owner/Jockey sau khi đua kết thúc nhưng trước khi công bố chính thức. Phán quyết xử lý thông báo ngược qua closed-loop.' },
            { id: 'J', title: 'Quản Lý Kết Quả và Công Bố Chính Thức (Admin)', icon: 'award', desc: 'Admin công bố kết quả (Unofficial → Official). Khóa cứng biên bản thi đấu. Tính nguyên tử ACID 1 Database Transaction duy nhất Rollback toàn cục.' },
            { id: 'K', title: 'Tính Toán và Phân Bổ Tiền Thưởng', icon: 'coins', desc: 'Tính toán phân bổ tiền thưởng theo quy tắc cấu hình. Admin cập nhật trạng thái thanh toán + audit log. Thanh toán tiền thật nằm ngoài hệ thống.' },
            { id: 'L', title: 'Bảng Xếp Hạng Tích Lũy (Leaderboard & Jockey Standings)', icon: 'bar-chart-2', desc: 'Leaderboard tự động xếp hạng ngựa và Jockey bằng HTTP Polling 30s. Không dùng WebSockets.' },
            { id: 'M', title: 'Quản Lý Dự Đoán và Prediction Gate', icon: 'target', desc: 'Admin cấu hình dự đoán Win và Place, phần thưởng, kiểm soát cổng. Mở cổng chỉ sau Post Position Draw (F4).' },
            { id: 'N', title: 'Đối Chiếu Dự Đoán và Trả Thưởng (Spectator)', icon: 'check-square', desc: 'Tự động đối chiếu dự đoán sau Official. Cộng điểm ảo Win/Place trực tiếp vào ví cá nhân.' },
            { id: 'O', title: 'Hệ Thống Thông Báo (Notification)', icon: 'bell', desc: 'Thông báo In-app và Email cho các sự kiện kích hoạt như từ chối, kết quả khiếu nại, kết quả đua, dự đoán, tiền thưởng. Không SMS.' },
            { id: 'P', title: 'Báo Cáo và Xuất Dữ Liệu', icon: 'printer', desc: 'Xuất người dùng theo role, ngựa, Jockey, kết quả, BXH, dự đoán, tiền thưởng định dạng CSV, PDF hoặc in.' },
            { id: 'Q', title: 'Bảo Mật, Xác Thực và Audit Log', icon: 'shield-alert', desc: 'Mã hóa JWT, Session Management, RBAC. Ghi Audit Log toàn bộ thao tác hệ thống quan trọng.' }
        ];"""
    content = re.sub(r'const IN_SCOPE_MODULES = \[[\s\S]*?\];', new_in_scope, content)

    # 3. Update OUT_SCOPE_ITEMS
    new_out_scope = """const OUT_SCOPE_ITEMS = [
            { id: '1', title: 'Thanh Toán Tiền Thưởng Thực Tế', tag: 'Finance', desc: 'Chỉ tính phân bổ; giao dịch tiền thật do BTC xử lý độc lập bên ngoài.' },
            { id: '2', title: 'WebSockets / Server-Sent Events', tag: 'Realtime', desc: 'Cập nhật bằng HTTP Polling 30s hoặc F5. Không dùng WebSockets duy trì liên tục.' },
            { id: '3', title: 'Thông Báo Qua SMS', tag: 'SMS', desc: 'Không tích hợp dịch vụ bên thứ ba. Chỉ In-app và Email.' },
            { id: '4', title: 'Dự Đoán Tổ Hợp Phức Tạp (Exotic Wager)', tag: 'Prediction', desc: 'Không hỗ trợ Exacta, Trifecta, Quinella, Superfecta. Chỉ hỗ trợ Win/Place.' },
            { id: '5', title: 'AI / Machine Learning', tag: 'Analytics', desc: 'Không xây dựng AI. Chỉ số phong độ là SQL Form Score tĩnh dựa trên trọng số.' },
            { id: '6', title: 'Tích Hợp Hệ Thống Thú Y Bên Ngoài', tag: 'Veterinary', desc: 'Dữ liệu y tế nhập thủ công; Không kết nối API bệnh viện thú y.' },
            { id: '7', title: 'Tích Hợp Phần Cứng Ngày Đua', tag: 'Hardware', desc: 'Không camera vạch đích, GPS ngựa hay đọc vi mạch. Nhập kết quả thủ công.' },
            { id: '8', title: 'Cá Cược Bằng Tiền Thật', tag: 'Gambling', desc: 'Tuyệt đối không Payment Gateway/Ví thật/Odds tài chính (Minigame phi tài chính).' },
            { id: '9', title: 'Tích Hợp Mạng Xã Hội', tag: 'Social', desc: 'Không chia sẻ kết quả trực tiếp lên mạng xã hội hay đăng nhập SSO (Google, FB).' },
            { id: '10', title: 'Quản Lý Huấn Luyện Viên', tag: 'Trainer', desc: 'Tích hợp chung quyền với Horse Owner, không có tài khoản và module độc lập.' },
            { id: '11', title: 'Livestreaming', tag: 'Media', desc: 'Không hỗ trợ video trực tiếp hoặc bình luận trực tuyến trong hệ thống.' },
            { id: '12', title: 'Hệ Thống Kế Toán Doanh Nghiệp', tag: 'Finance', desc: 'Không tích hợp Xero/QuickBooks hay báo cáo thu chi chi tiết.' }
        ];"""
    content = re.sub(r'const OUT_SCOPE_ITEMS = \[[\s\S]*?\];', new_out_scope, content)

    # 4. Update phaseData
    new_phase_data = """const phaseData = {
            1: {
                title: "① Khởi tạo giải đấu",
                actions: {
                    admin: ["Tạo giải đấu với thông tin thô (thời gian, cự ly, TrackType, AllowedBreed)", "Lập cấu trúc các vòng đua (Vòng loại &rarr; Bán kết &rarr; Chung kết)", "Cấu hình Quỹ tiền thưởng (Purse) tương ứng từng cuộc đua"],
                    owner: [],
                    jockey: [],
                    referee: [],
                    spectator: ["Xem thông tin giải đấu mới được tạo và cấu trúc vòng đua công khai"]
                },
                rules: [
                    "<strong>Giống ngựa cho phép:</strong> Thoroughbred, Arabian, Quarter Horse, Mixed.",
                    "<strong>Quỹ tiền thưởng:</strong> Được thiết lập bằng VND làm căn cứ chia thưởng ngoại tuyến, không thực hiện giao dịch thanh toán trực tiếp."
                ],
                design: "Thiết kế thực thể cơ sở dữ liệu `Tournament` và `Race` liên kết 1-nhiều. Hệ thống hiển thị sơ đồ cây các vòng đua trực quan trên Admin Dashboard.",
                simState: { tournament: "Đã Khởi Tạo", gate: "Đóng", coi: "Chưa kiểm tra", jockey: "Chưa kiểm tra" },
                terminalLogs: [
                    "[SYSTEM] Khởi chạy Giai đoạn 1: Thiết lập cơ cấu giải đua mới...",
                    "[DB] INSERT INTO Tournaments (Name, AllowedBreed, TrackType) VALUES ('Horse Racing Cup', 'Thoroughbred|Mixed', 'Turf')",
                    "[SYSTEM] Tạo giải đấu và phân bộ quỹ Purse 50.000.000 VND thành công!"
                ],
                simNoti: { role: "Spectator", text: "🔔 Giải đấu mới đã được ban tổ chức công bố công khai trên hệ thống!" },
                flowNodes: [
                    { id: '1-1', label: '1.1. Đăng ký & Phân quyền|Quyền RBAC', x: 50, y: 50, actor: 'admin' },
                    { id: '1-2', label: '1.2. Tạo Giải Đấu|TrackType & Distance', x: 230, y: 50, actor: 'admin' },
                    { id: '1-3', label: '1.3. Lập Sơ Đồ Vòng Đua|Vòng loại -> Chung kết', x: 410, y: 50, actor: 'admin' },
                    { id: '1-4', label: '1.4. Phân Bổ Quỹ Purse|Tỷ lệ chia 100%', x: 590, y: 50, actor: 'admin' },
                    { id: '1-5', label: '1.5. Công Bố Giải Đấu|Trạng thái OpenReg', x: 770, y: 530, actor: 'spectator' }
                ],
                flowConnections: [
                    { src: '1-1', dst: '1-2' },
                    { src: '1-2', dst: '1-3' },
                    { src: '1-3', dst: '1-4' },
                    { src: '1-4', dst: '1-5' }
                ]
            },
            2: {
                title: "② Đăng ký tham gia",
                actions: {
                    admin: ["Kiểm duyệt hồ sơ ngựa thi đấu dựa trên giống ngựa AllowedBreed", "Từ chối và điền lý do từ chối để hệ thống tự động gửi thông báo cho Chủ ngựa"],
                    owner: ["Khai báo hồ sơ ngựa (Tên, giống, cân nặng)", "Tìm kiếm Jockey và chốt ghép cặp", "Nộp hồ sơ ngựa ứng tuyển vào giải đấu"],
                    jockey: ["Khai báo chứng chỉ hành nghề khi tạo tài khoản", "Xác nhận/Từ chối từng lời mời thuê từ phía các Chủ ngựa"],
                    referee: [],
                    spectator: []
                },
                rules: [
                    "<strong>Tách Luồng Phê Duyệt (F1):</strong> Bước duyệt hồ sơ ngựa của Admin hoàn toàn KHÔNG bao gồm việc kiểm tra chứng chỉ của Jockey.",
                    "<strong>Ràng buộc lý do từ chối:</strong> Bắt buộc nhập lý do từ chối phê duyệt hồ sơ tối thiểu 10 ký tự."
                ],
                design: "Duy trì trạng thái hồ sơ ngựa qua các enum: `Pending`, `Approved`, `Rejected`. Khi ở trạng thái `Rejected`, bắt buộc giao diện hiển thị trường nhập chuỗi `reason` gửi trực tiếp vào bảng Notification.",
                simState: { tournament: "Đăng ký", gate: "Đóng", coi: "Chưa kiểm tra", jockey: "Chưa kiểm tra" },
                terminalLogs: [
                    "[SYSTEM] Giai đoạn 2: Cổng đăng ký mở dành cho Horse Owner và Jockey.",
                    "[API] POST /api/horses -> Đăng ký ngựa 'Thần Phong' (Allowed Breed)",
                    "[JOCKEY] Gửi lời mời đến Jockey Nguyễn Văn A (Chứng chỉ: JC-992)"
                ],
                simNoti: { role: "Horse Owner", text: "🔔 Jockey Nguyễn Văn A đã chấp thuận lời mời điều khiển ngựa của bạn!" },
                flowNodes: [
                    { id: '2-1', label: '2.1. Jockey Khai Hồ Sơ|Chứng chỉ hành nghề', x: 50, y: 290, actor: 'jockey' },
                    { id: '2-2', label: '2.2. Khai Báo Ngựa|Tên & Giống', x: 50, y: 170, actor: 'owner' },
                    { id: '2-3', label: '2.3. Owner Mời Jockey|Gửi lời mời & Chốt', x: 230, y: 170, actor: 'owner' },
                    { id: '2-4', label: '2.4. Nộp Hồ Sơ Đăng Ký|Gửi Đơn Lên Hệ Thống', x: 410, y: 170, actor: 'owner' },
                    { id: '2-5', label: '2.5. Admin Phê Duyệt|Tách biệt duyệt F1', x: 620, y: 50, actor: 'admin', type: 'checkpoint', errorId: 'horse_reg_rejected' },
                    { id: '2-5-ERR', label: '2.5-ERR: Bị Từ Chối|Lý do >=10 kí tự', x: 620, y: 170, actor: 'owner', type: 'error', errorId: 'horse_reg_rejected' },
                    { id: '2-6', label: '2.6. Nhận Kết Quả Duyệt|Approved', x: 800, y: 170, actor: 'owner' }
                ],
                flowConnections: [
                    { src: '2-1', dst: '2-3' },
                    { src: '2-2', dst: '2-3' },
                    { src: '2-3', dst: '2-4' },
                    { src: '2-4', dst: '2-5' },
                    { src: '2-5', dst: '2-6', errorId: 'horse_reg_rejected' },
                    { src: '2-5', dst: '2-5-ERR', isErrorBranch: true, errorId: 'horse_reg_rejected' },
                    { src: '2-5-ERR', dst: '2-6', isErrorBranch: true, errorId: 'horse_reg_rejected' }
                ]
            },
            3: {
                title: "③ Chuẩn bị cuộc đua",
                actions: {
                    admin: ["Phân bổ cặp đấu vào lượt chạy", "Bốc thăm Post Position ngẫu nhiên", "Phân công Trọng tài COI Check", "Mở cổng dự đoán"],
                    owner: ["Xác nhận tham gia lịch đua trước giờ chốt 24h"],
                    jockey: ["Tra cứu lịch đua"],
                    referee: ["Nhận thông báo nhiệm vụ điều khiển"],
                    spectator: ["Gửi dự đoán Win hoặc Place lên hệ thống (Prediction Gate Open)"]
                },
                rules: [
                    "<strong>Phân công Trọng tài (F2):</strong> Phải phân công ban trọng tài ít nhất 5 ngày làm việc trước ngày đua, kiểm tra xung đột lợi ích COI.",
                    "<strong>Mở cổng dự đoán (F4):</strong> Cổng dự đoán chỉ mở sau khi hoàn tất bốc thăm vị trí xuất phát."
                ],
                design: "Scheduler của hệ thống quét database tự động chuyển trạng thái `Cancelled` và giải phóng cổng chạy `Vacant` nếu quá hạn xác nhận 24h.",
                simState: { tournament: "Chuẩn Bị", gate: "MỞ (Open)", coi: "Hợp lệ", jockey: "Chưa kiểm tra" },
                terminalLogs: [
                    "[SYSTEM] Giai đoạn 3: Phân bổ ngựa và phân công ban Trọng tài.",
                    "[COI-CHECK] OK: Trọng tài chính Trần Văn B không có xung đột với Chủ ngựa nào.",
                    "[SYSTEM] Bốc thăm Post Position thành công. Cổng dự đoán Win/Place mở."
                ],
                simNoti: { role: "Race Referee", text: "🔔 Ban tổ chức chỉ định bạn làm Trọng tài chính cuộc đua R-01!" },
                flowNodes: [
                    { id: '3-1', label: '3.1. Phân Bổ Lượt Chạy|Sắp xếp cuộc đua', x: 20, y: 50, actor: 'admin' },
                    { id: '3-2', label: '3.2. Bốc Thăm Post Draw|Xác định cổng xuất phát', x: 200, y: 50, actor: 'admin' },
                    { id: '3-3', label: '3.3. Xác Nhận Lịch Chạy|Trước giờ đua 24h', x: 380, y: 170, actor: 'owner', type: 'checkpoint', errorId: 'owner_missed_confirmation' },
                    { id: '3-3-ERR', label: '3.3-ERR: Rút/Quá Hạn|Cổng Vacant/Cancelled', x: 380, y: 240, actor: 'owner', type: 'error', errorId: 'owner_missed_confirmation' },
                    { id: '3-5', label: '3.5. COI Check Trọng Tài|Kiểm tra xung đột', x: 560, y: 50, actor: 'admin', type: 'checkpoint', errorId: 'coi_conflict_detected' },
                    { id: '3-5-ERR', label: '3.5-ERR: Xung Đột COI|Chặn phân công', x: 560, y: 120, actor: 'admin', type: 'error', errorId: 'coi_conflict_detected' },
                    { id: '3-4', label: '3.4. Tra Cứu Lịch Chạy|Jockey xem lịch', x: 560, y: 290, actor: 'jockey' },
                    { id: '3-6', label: '3.6. Nhận Nhiệm Vụ|Referee chuẩn bị', x: 780, y: 410, actor: 'referee' },
                    { id: '3-7', label: '3.7. Mở Cổng Dự Đoán|Ràng buộc F4', x: 380, y: 530, actor: 'spectator' },
                    { id: '3-8', label: '3.8. Đặt Dự Đoán|Win / Place (F6)', x: 650, y: 530, actor: 'spectator' }
                ],
                flowConnections: [
                    { src: '3-1', dst: '3-2' },
                    { src: '3-2', dst: '3-3' },
                    { src: '3-2', dst: '3-5' },
                    { src: '3-2', dst: '3-7' },
                    { src: '3-3', dst: '3-4', errorId: 'owner_missed_confirmation' },
                    { src: '3-3', dst: '3-3-ERR', isErrorBranch: true, errorId: 'owner_missed_confirmation' },
                    { src: '3-5', dst: '3-6', errorId: 'coi_conflict_detected' },
                    { src: '3-5', dst: '3-5-ERR', isErrorBranch: true, errorId: 'coi_conflict_detected' },
                    { src: '3-4', dst: '3-6' },
                    { src: '3-7', dst: '3-8' }
                ]
            },
            4: {
                title: "④ Trước giờ đua (Pre-race)",
                actions: {
                    admin: [],
                    owner: [],
                    jockey: [],
                    referee: ["Xác minh danh tính ngựa paddock", "Ghi nhận sức khỏe y tế thủ công", "Chạy Jockey Independence Check", "Truất quyền thi đấu ngựa vi phạm"],
                    spectator: ["Xem lại dự đoán (Cổng dự đoán ở trạng thái Locked)"]
                },
                rules: [
                    "<strong>Jockey Independence:</strong> Jockey không có quan hệ trực hệ với các Owner đối thủ.",
                    "<strong>Xử lý Truất Quyền (DISQ):</strong> Đổi trạng thái RaceEntry thành Disqualified, tự động gửi 3 thông báo, hoàn điểm ảo cho Spectator."
                ],
                design: "Xây dựng màn hình Paddock Check-in dành riêng cho Trọng tài. Nếu phát hiện vi phạm, bẻ luồng sang loại khẩn cấp và hoàn tiền Spectator trước giờ G.",
                simState: { tournament: "Xác Minh", gate: "Khóa (Locked)", coi: "Hợp lệ", jockey: "Đã kiểm tra (Hợp lệ)" },
                terminalLogs: [
                    "[SYSTEM] Giai đoạn 4: Trọng tài thực hiện kiểm soát tại paddock...",
                    "[JOCKEY-INDEPENDENCE] Kiểm tra quan hệ gia đình trực hệ nài ngựa...",
                    "[SYSTEM] Toàn bộ ngựa và Jockey đạt chuẩn. Khóa cổng cược tự động."
                ],
                simNoti: { role: "Spectator", text: "🔔 Cổng dự đoán đã khóa tự động ngay trước giờ G." },
                flowNodes: [
                    { id: '4-1', label: '4.1. Khóa Cổng Dự Đoán|Khóa tự động', x: 50, y: 530, actor: 'spectator' },
                    { id: '4-2', label: '4.2. Khớp Danh Tính|Paddock check', x: 50, y: 340, actor: 'referee', type: 'checkpoint', errorId: 'identity_mismatch' },
                    { id: '4-3', label: '4.3. Y Tế Thủ Công|Thú y xác nhận (F3)', x: 50, y: 410, actor: 'referee', type: 'checkpoint', errorId: 'horse_health_unfit' },
                    { id: '4-4', label: '4.4. Độc Lập Nài Ngựa|Check quan hệ', x: 50, y: 480, actor: 'referee', type: 'checkpoint', errorId: 'jockey_independence_conflict' },
                    { id: '4-5-DISQ', label: '4.5-DISQ: TRUẤT QUYỀN KHẨN CẤP|Gửi 3 thông báo & Hoàn điểm cược', x: 380, y: 290, actor: 'jockey', type: 'error', errorId: 'identity_mismatch', w: 200 },
                    { id: '4-5', label: '4.5. Xác Nhận Chạy|Chốt danh sách', x: 740, y: 410, actor: 'referee' }
                ],
                flowConnections: [
                    { src: '4-2', dst: '4-5', errorId: 'identity_mismatch' },
                    { src: '4-3', dst: '4-5', errorId: 'horse_health_unfit' },
                    { src: '4-4', dst: '4-5', errorId: 'jockey_independence_conflict' },
                    { src: '4-2', dst: '4-5-DISQ', isErrorBranch: true, errorId: 'identity_mismatch' },
                    { src: '4-3', dst: '4-5-DISQ', isErrorBranch: true, errorId: 'horse_health_unfit' },
                    { src: '4-4', dst: '4-5-DISQ', isErrorBranch: true, errorId: 'jockey_independence_conflict' },
                    { src: '4-1', dst: '4-5' }
                ]
            },
            5: {
                title: "⑤ Diễn biến cuộc đua (Live)",
                actions: {
                    admin: [],
                    owner: ["Nộp đơn khiếu nại Protest"],
                    jockey: ["Nộp đơn khiếu nại Protest"],
                    referee: ["Bấm lệnh LIVE Start", "Ghi nhận lỗi vi phạm trên sân bằng dropdown mã vi phạm", "Tiếp nhận và xử lý khiếu nại Protest", "Xác nhận kết quả sơ bộ và chốt biên bản"],
                    spectator: ["Theo dõi trạng thái cuộc đua trực tiếp trên Web bằng Live Simulation"]
                },
                rules: [
                    "<strong>Live Simulation (Animation):</strong> Sử dụng Math.random() di chuyển chip ngựa trên canvas, tuyệt đối không dùng WebSockets.",
                    "<strong>Khiếu nại Protest:</strong> Trọng tài chốt xử lý đóng vòng (closed-loop), gửi thông báo kết quả cho cả 2 bên."
                ],
                design: "Menu 7 mã lỗi vi phạm đặc thù ngành đua ngựa cho phép Trọng tài ghi nhận biên bản nhanh. Chỉ được sửa đổi trước khi chốt kết quả sơ bộ.",
                simState: { tournament: "LIVE", gate: "Khóa cứng", coi: "Hợp lệ", jockey: "Hợp lệ" },
                terminalLogs: [
                    "[SYSTEM] Giai đoạn 5: Phát súng xuất phát cuộc đua R-01 LIVE!",
                    "[API] POST /api/referee/violation -> Ghi nhận lỗi chèn ép đường đua",
                    "[SYSTEM] Cuộc đua kết thúc sơ bộ. Trọng tài tiếp nhận đơn khiếu nại Protest."
                ],
                simNoti: { role: "Jockey", text: "🔔 Trọng tài đã ghi nhận lỗi vi phạm chèn ép (E-02) trong cuộc đua." },
                flowNodes: [
                    { id: '5-1', label: '5.1. Bấm LIVE Start|Trạng thái LIVE', x: 50, y: 410, actor: 'referee' },
                    { id: '5-2', label: '5.2. Khán Giả Xem Live|Mô phỏng canvas (F5)', x: 230, y: 530, actor: 'spectator' },
                    { id: '5-live-btn', label: '▶ XEM MÔ PHỎNG LÀN CHẠY', x: 50, y: 600, actor: 'spectator', w: 180, h: 40 },
                    { id: '5-3', label: '5.3. Ghi Lỗi Vi Phạm|Chọn dropdown mã', x: 230, y: 410, actor: 'referee' },
                    { id: '5-4', label: '5.4. Nộp Đơn Protest|Owner / Jockey', x: 230, y: 170, actor: 'owner' },
                    { id: '5-5', label: '5.5. Giải Quyết Protest|Bác bỏ / Chấp thuận', x: 450, y: 410, actor: 'referee', type: 'checkpoint', errorId: 'protest_approved' },
                    { id: '5-5-ERR', label: '5.5-ERR: Chấp Thuận|Place Behind / DISQ', x: 450, y: 340, actor: 'referee', type: 'error', errorId: 'protest_approved' },
                    { id: '5-6', label: '5.6. Chốt Kết Quả|Sơ bộ Unofficial', x: 750, y: 410, actor: 'referee' }
                ],
                flowConnections: [
                    { src: '5-1', dst: '5-2' },
                    { src: '5-1', dst: '5-3' },
                    { src: '5-2', dst: '5-6' },
                    { src: '5-3', dst: '5-5' },
                    { src: '5-4', dst: '5-5' },
                    { src: '5-5', dst: '5-6', errorId: 'protest_approved' },
                    { src: '5-5', dst: '5-5-ERR', isErrorBranch: true, errorId: 'protest_approved' },
                    { src: '5-5-ERR', dst: '5-6', isErrorBranch: true, errorId: 'protest_approved' }
                ]
            },
            6: {
                title: "⑥ Công bố kết quả & Trả thưởng",
                actions: {
                    admin: ["Phê duyệt kết quả Unofficial -> Official", "Cấu hình phân bổ Purse", "Ghi nhận trạng thái thanh toán thủ công ngoại tuyến"],
                    owner: ["Nhận phân bổ tiền thưởng Purse", "Xem BXH Ngựa"],
                    jockey: ["Nhận thu nhập Jockey", "Xem BXH Jockey Standings qua Polling 30s"],
                    referee: ["Xem biên bản lưu trữ cố định"],
                    spectator: ["Nhận kết quả cược Win/Place (+200/+100 điểm ảo)"]
                },
                rules: [
                    "<strong>Nguyên tử ACID:</strong> Lỗi tại bất kỳ tác vụ nào trong 6 bước cập nhật kết quả sẽ Rollback toàn bộ dữ liệu.",
                    "<strong>Thanh toán tiền thật:</strong> Nằm ngoài hệ thống (F5). Admin ghi Audit Log ngoại tuyến."
                ],
                design: "Bảng xếp hạng cập nhật tự động bằng Polling 30 giây thay vì WebSockets để đảm bảo tính gọn nhẹ và bảo mật.",
                simState: { tournament: "OFFICIAL", gate: "Khóa cứng", coi: "Hợp lệ", jockey: "Hợp lệ" },
                terminalLogs: [
                    "[SYSTEM] Giai đoạn 6: Bắt đầu chuỗi 6 tác vụ declare Official...",
                    "[DB] UPDATE Races SET Status='Official' WHERE Id='R-01'",
                    "[SYSTEM] Tự động đối chiếu cược, trả thưởng và cập nhật Leaderboard thành công!"
                ],
                simNoti: { role: "Spectator", text: "🔔 Dự đoán chính xác! Nhận 200 điểm ảo thành công." },
                flowNodes: [
                    { id: '6-1', label: '6.1. Declare Official|Transaction ACID', x: 20, y: 50, actor: 'admin', type: 'checkpoint', errorId: 'transaction_rollback' },
                    { id: '6-1-ERR', label: '6.1-ERR: Lỗi Rollback|Rollback ACID', x: 20, y: 120, actor: 'admin', type: 'error', errorId: 'transaction_rollback' },
                    { id: '6-2', label: '6.2. Khóa Biên Bản|Không thể sửa', x: 220, y: 50, actor: 'admin' },
                    { id: '6-3', label: '6.3. Cập Nhật Leaderboard|Polling 30s', x: 440, y: 290, actor: 'jockey' },
                    { id: '6-4', label: '6.4. Trả Thưởng Ví Ảo|Cộng điểm Spectator', x: 440, y: 530, actor: 'spectator' },
                    { id: '6-5', label: '6.5. Phân Bổ Quỹ Purse|Lưu vết lý thuyết', x: 440, y: 170, actor: 'owner' },
                    { id: '6-6', label: '6.6. Thanh Toán Offline|Ghi Audit Log', x: 660, y: 50, actor: 'admin' },
                    { id: '6-7', label: '6.7. Báo Cáo Thống Kê|Xuất PDF/CSV', x: 860, y: 50, actor: 'admin' }
                ],
                flowConnections: [
                    { src: '6-1', dst: '6-2', errorId: 'transaction_rollback' },
                    { src: '6-1', dst: '6-1-ERR', isErrorBranch: true, errorId: 'transaction_rollback' },
                    { src: '6-2', dst: '6-3' },
                    { src: '6-2', dst: '6-4' },
                    { src: '6-2', dst: '6-5' },
                    { src: '6-5', dst: '6-6' },
                    { src: '6-6', dst: '6-7' },
                    { src: '6-3', dst: '6-7' },
                    { src: '6-4', dst: '6-7' }
                ]
            }
        };"""
    content = re.sub(r'const phaseData = \{.*?\n\s*\};\s*/\* =', new_phase_data + '\n/* =', content, flags=re.DOTALL)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    update_index()
