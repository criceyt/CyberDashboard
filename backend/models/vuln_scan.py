from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Text

Base = declarative_base()

class VulnScan(Base):
    __tablename__ = 'vuln_scan'
    id = Column(Integer, primary_key=True)
    host = Column(String(100))
    scan_type = Column(String(50))
    timestamp = Column(DateTime)
    vulnerabilities = Column(Text)
    json_report_path = Column(String(255))
    html_report_path = Column(String(255))
