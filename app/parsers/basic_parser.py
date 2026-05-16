
sample_data = "[WARNING] CPU usage high"
    
class BasicParser:
    def parse(self, log: dict) -> dict:
        raw_line = log. get("raw_line" "")
        if not raw_line:
            log["severity"] = "Unknown"
            log["message"] = ""
            return log
        parts = raw_line.split()
        severity = "Unknown"
        message = raw_line
        if parts and parts[0].startswith("[") and parts[0].endswith("]"):
            severity = parts[0].strip("[]")
            message = " ".join(parts[1:]) if len(parts) > 1 else ""
        
        log["event_type"] = "log"
        log["severity"] = severity
        log["message"] = message
        return log
        








