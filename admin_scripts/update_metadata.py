import os
from supabase import create_client, Client
import argparse
from typing import Optional
from dotenv import load_dotenv, dotenv_values
from pathlib import Path

# 初始化 Supabase client
current_dir = Path(__file__).parent.absolute()
env_path = os.path.join(current_dir.parent, 'server', '.env')
print(env_path)

# 使用 dotenv_values() 直接讀取 .env 檔案內容
config = dotenv_values(env_path)

# 使用 config 字典來取得環境變數
supabase: Client = create_client(
    config.get("SUPABASE_URL"), 
    config.get("SUPABASE_SERVICE_ROLE_KEY")  # 直接使用 service role key
)

def update_user_metadata(email: str, password: str, role: str) -> None:
    """更新用戶的 metadata"""
    try:
        # 先用 admin API 取得用戶資料
        users_response = supabase.auth.admin.list_users()
        # print(users_response)
        
        # users_response 直接就是用戶列表
        target_user = next((user for user in users_response if user.email == email), None)
        
        if not target_user:
            raise ValueError(f"User with email {email} not found")
            
        # 驗證role參數
        if role not in ["admin", "reporter"]:
            raise ValueError("Role must be either 'admin' or 'reporter'")
            
        # 取得現有的 metadata
        current_metadata = target_user.user_metadata or {}
        
        # 更新metadata,加入system_role
        new_metadata = {
            **current_metadata,
            "system_role": role
        }
        
        # 使用admin API更新用戶
        supabase.auth.admin.update_user_by_id(
            target_user.id,
            {"user_metadata": new_metadata}
        )
        
        print(f"Successfully updated metadata for user {email}")
        print(f"New metadata: {new_metadata}")
        
    except Exception as e:
        print(f"Error updating user metadata: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Update Supabase user metadata')
    parser.add_argument('--email', required=True, help='User email')
    parser.add_argument('--password', required=True, help='User password')
    parser.add_argument('--role', required=True, choices=['admin', 'reporter'], 
                      help='System role to assign (admin or reporter)')
    
    args = parser.parse_args()
    
    update_user_metadata(args.email, args.password, args.role)

# cli usage: python update_metadata.py --email <email> --password <password> --role <role>
if __name__ == "__main__":
    main()
