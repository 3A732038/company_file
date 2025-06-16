# ===== 建立職級層級 =====

# 定義職級：CEO > 總監 > 經理 > 資深 > 一般員工
job_level:ceo#holder@user:ceo_wang
job_level:ceo#organization@organization:techcorp

job_level:director#holder@user:engineering_director
job_level:director#holder@user:marketing_director
job_level:director#holder@user:hr_director
job_level:director#holder@user:sales_director
job_level:director#organization@organization:techcorp

job_level:manager#holder@user:tech_lead
job_level:manager#holder@user:marketing_manager
job_level:manager#holder@user:project_manager_alex
job_level:manager#organization@organization:techcorp

job_level:senior#holder@user:senior_engineer_john
job_level:senior#holder@user:senior_engineer_lisa
job_level:senior#holder@user:senior_designer_mike
job_level:senior#organization@organization:techcorp

job_level:regular#holder@user:engineer_mary
job_level:regular#holder@user:engineer_tom
job_level:regular#holder@user:designer_anna
job_level:regular#organization@organization:techcorp

# 建立職級層級關係（高職級包含低職級權限）
job_level:ceo#senior_to@job_level:director
job_level:director#senior_to@job_level:manager  
job_level:manager#senior_to@job_level:senior
job_level:senior#senior_to@job_level:regular

# ===== 建立安全等級 =====

# L1: 一般員工可看（公開文件）
security_level:level_1#required_job_level@job_level:regular
security_level:level_1#admin@user:content_manager

# L2: 資深員工以上可看
security_level:level_2#required_job_level@job_level:senior  
security_level:level_2#admin@user:tech_lead

# L3: 經理級以上可看
security_level:level_3#required_job_level@job_level:manager
security_level:level_3#admin@user:hr_director

# L4: 總監級以上可看
security_level:level_4#required_job_level@job_level:director
security_level:level_4#admin@user:ceo_wang

# L5: 僅 CEO 可看（最高機密）
security_level:level_5#required_job_level@job_level:ceo
security_level:level_5#admin@user:ceo_wang

# ===== 建立具體文件並指定安全等級 =====

# 公司手冊 (L1: 所有員工可看)
resource:company_handbook#owner@user:hr_director
resource:company_handbook#security_level@security_level:level_1
resource:company_handbook#parent_department@department:hr

# 技術規範文件 (L2: 資深員工以上可看)
resource:tech_standards#owner@user:tech_lead
resource:tech_standards#security_level@security_level:level_2
resource:tech_standards#parent_department@department:engineering

# 部門預算資料 (L3: 經理級以上可看)
resource:department_budget#owner@user:engineering_director
resource:department_budget#security_level@security_level:level_3
resource:department_budget#parent_department@department:engineering

# 公司策略規劃 (L4: 總監級以上可看)
resource:company_strategy_2024#owner@user:ceo_wang
resource:company_strategy_2024#security_level@security_level:level_4
resource:company_strategy_2024#parent_organization@organization:techcorp

# 併購計畫 (L5: 僅 CEO 可看)
resource:merger_plan#owner@user:ceo_wang
resource:merger_plan#security_level@security_level:level_5
resource:merger_plan#parent_organization@organization:techcorp

# 員工薪資表 (L4: 總監級以上，但 HR 總監擁有)
resource:salary_report#owner@user:hr_director
resource:salary_report#security_level@security_level:level_4
resource:salary_report#parent_department@department:hr

# 專案提案 (L3: 經理級以上，但專案成員可看)
resource:project_proposal_alpha#owner@user:project_manager_alex
resource:project_proposal_alpha#security_level@security_level:level_3
resource:project_proposal_alpha#viewer@user:senior_engineer_john  # 特別授權給專案成員
resource:project_proposal_alpha#parent_project@project:alpha

# API 密鑰文件 (L2: 資深工程師以上)
resource:api_keys#owner@user:tech_lead
resource:api_keys#security_level@security_level:level_2
resource:api_keys#parent_department@department:engineering

# 客戶合約 (L3: 經理級以上，但業務團隊可看)
resource:client_contract_abc#owner@user:sales_director
resource:client_contract_abc#security_level@security_level:level_3
resource:client_contract_abc#viewer@user:sales_manager      # 業務經理
resource:client_contract_abc#viewer@user:account_manager    # 客戶經理
resource:client_contract_abc#parent_department@department:sales

# 績效評估標準 (L3: 經理級以上)
resource:performance_criteria#owner@user:hr_director
resource:performance_criteria#security_level@security_level:level_3
resource:performance_criteria#parent_department@department:hr

# 競爭對手分析 (L4: 總監級以上)
resource:competitor_analysis#owner@user:marketing_director
resource:competitor_analysis#security_level@security_level:level_4
resource:competitor_analysis#parent_department@department:marketing

# 日常工作文件 (L1: 所有員工，特定團隊編輯)
resource:team_meeting_notes#owner@user:project_manager_alex
resource:team_meeting_notes#security_level@security_level:level_1
resource:team_meeting_notes#editor@usergroup:project_alpha_team#member
resource:team_meeting_notes#parent_project@project:alpha