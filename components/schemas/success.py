# Define the Success schema in the components section
success_model = api.model("Success", {
    "message": fields.String(description="Success message")
})