import zmail
import os


mail_content = {
    "subject": "简报",
        }


def send_mail_info(report, report_file_path):
    mail_content["content_html"] = f"<html><div><p>{report}</p><a src={report_file_path}>点击下载</a></div></html>"

    server = zmail.server("529895353@qq.com", os.environ.get("QQ_EMAIL_CODE"))
    server.send_mail("529895353@qq.com", mail_content)

if __name__=="__main__":
    report = "12345678978978789"
    send_mail_info(report)