from datetime import datetime

class AuditLogger:
    
    def __init__(self, spark, storage_account, pipeline_name, notebook_name):
        self.spark = spark
        self.audit_path = f"abfss://datalake@{storage_account}.dfs.core.windows.net/audit/pipeline_runs"
        self.pipeline_name = pipeline_name
        self.notebook_name = notebook_name
        self.start_time = datetime.now()
    
    def log_success(self, rows_read, rows_written, rows_quarantined=0):
        self._write_log(
            status="success",
            rows_read=rows_read,
            rows_written=rows_written,
            rows_quarantined=rows_quarantined,
            error_message=None
        )
    
    def log_failure(self, error_message, rows_read=0):
        self._write_log(
            status="failed",
            rows_read=rows_read,
            rows_written=0,
            rows_quarantined=0,
            error_message=str(error_message)
        )
    
    def _write_log(self, status, rows_read, rows_written, rows_quarantined, error_message):
        end_time = datetime.now()
        duration = (end_time - self.start_time).seconds
        
        quarantine_rate = round(
            rows_quarantined / rows_read * 100, 2
        ) if rows_read > 0 else 0
        
        log_df = self.spark.createDataFrame([{
            "pipeline_name":       self.pipeline_name,
            "notebook_name":       self.notebook_name,
            "start_time":          str(self.start_time),
            "end_time":            str(end_time),
            "duration_seconds":    duration,
            "rows_read":           rows_read,
            "rows_written":        rows_written,
            "rows_quarantined":    rows_quarantined,
            "quarantine_rate_pct": quarantine_rate,
            "status":              status,
            "error_message":       error_message if error_message else "",
            "environment":         "dev",
            "batch_date":          end_time.strftime("%Y-%m-%d")
        }])
        
        log_df.write.format("delta") \
            .mode("append") \
            .save(self.audit_path)
        
        print(f"[Audit] {self.notebook_name} → {status} | rows_in={rows_read} | rows_out={rows_written} | quarantined={rows_quarantined} | duration={duration}s")