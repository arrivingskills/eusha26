import datetime

# 1. Define the curried function structure
def create_logger(environment: str):
    def for_service(service_name: str):
        def with_level(level: str):
            def log(message: str):
                # The final execution function that has access to all bundled context
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{timestamp}] [{environment.upper()}] [{level.upper()}] ({service_name}): {message}")
            return log
        return with_level
    return for_service

# --- HOW TO USE IT IN REAL WORLD LAYERS ---

# Layer 1: Infrastructure Setup (Happens at global app initialization)
# The DevOps/Infra layer configures the environment.
prod_logger = create_logger("production")
staging_logger = create_logger("staging")

# Layer 2: Microservice Bootstrapping (Happens when a specific service starts)
# The Payment Service team configures their specific service name.
payment_service_logger = prod_logger("payment-processor")
auth_service_logger = staging_logger("user-auth")

# Layer 3: Module Level (Happens inside specific code files/modules)
# Developers create specific log level functions for their modules.
payment_error = payment_service_logger("error")
payment_info = payment_service_logger("info")
auth_debug = auth_service_logger("debug")

# Layer 4: Application Runtime (Happens deep inside business logic)
# The actual business logic execution only cares about the final message.
payment_info("Connection to payment gateway established successfully.")
payment_error("Credit card transaction failed: Timeout.")
auth_debug("User 'johndoe' token successfully validated.")

# not:
# log_message("production", "payment-processor", "error", "Gateway timeout.")