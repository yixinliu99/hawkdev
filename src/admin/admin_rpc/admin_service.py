from concurrent import futures
import grpc
from admin.dao.mongoDAO import MongoDAO
from datetime import datetime, timedelta
from admin.admin_rpc.admin_service_pb2 import (
    Response,
    FlaggedItemsResponse,
    ActiveAuctionsResponse,
    FlaggedItem,
    Auction,
    Email,
    UnrespondedEmailsResponse
)
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from admin.consts.consts import *
import admin.admin_rpc.admin_service_pb2_grpc as admin_service_pb2_grpc


class AdminService(admin_service_pb2_grpc.AdminServiceServicer):
    def __init__(self):
        # self.dao = MongoDAO()
        self.dao = None

    def StopAuctionEarly(self, request, context):
        result = self.dao.stop_auction_early(request.auction_id)
        if result.modified_count:
            return Response(message="Auction stopped successfully.")
        return Response(message="Auction not found or already stopped.")

    def RemoveAndBlockUser(self, request, context):
        user_result, auction_count = self.dao.block_user_and_remove_auctions(request.user_id)
        if user_result:
            return Response(
                message=f"User blocked and {auction_count} auctions removed."
            )
        return Response(message="User not found or already blocked.")

    def AddModifyRemoveCategory(self, request, context):
        if request.action == "add":
            self.dao.add_category(request.category_id, request.category_name)
            return Response(message="Category added.")
        elif request.action == "modify":
            result = self.dao.modify_category(request.category_id, request.category_name)
            if result.modified_count:
                return Response(message="Category modified.")
            return Response(message="Category not found.")
        elif request.action == "remove":
            result = self.dao.remove_category(request.category_id)
            if result.deleted_count:
                return Response(message="Category removed.")
            return Response(message="Category not found.")
        return Response(message="Invalid action.")

    def ViewFlaggedItems(self, request, context):
        flagged_items = self.dao.get_flagged_items()
        items = [
            FlaggedItem(
                name=item["name"],
                description=item.get("description", "No description available"),
                category=item.get("category", "Uncategorized"),
                flag_reason=item.get("flag_reason", "Unknown reason"),
                flagged_date=item.get("flagged_date", "").isoformat() if "flagged_date" in item else "N/A"
            )
            for item in flagged_items
        ]
        print(items)
        return FlaggedItemsResponse(flagged_items=items)

    def ViewActiveAuctions(self, request, context):
        print("View active auctions")
        active_auctions = self.dao.get_active_auctions(sort_by=request.sort_by)

        # Convert MongoDB results to gRPC response
        auctions = [
            Auction(
                title=auction["title"],
                description=auction["description"],
                starting_price=auction["starting_price"],
                current_price=auction["current_price"],
                start_time=auction["start_time"].isoformat(),  # Convert datetime to string
                end_time=auction["end_time"].isoformat(),
                category=auction["category"]
            )
            for auction in active_auctions
        ]

        return ActiveAuctionsResponse(auctions=auctions)

    def ExamineMetrics(self, request, context):
        timeframe_days = request.days + (request.weeks * 7) + (request.months * 30)

        # Query MongoDB for auctions closed in the calculated timeframe
        start_date = datetime.utcnow() - timedelta(days=timeframe_days)

        closed_auctions = self.dao.get_closed_auctions(start_date)
        auctions = [
            Auction(
                title=auction["title"],
                description=auction["description"],
                starting_price=auction["starting_price"],
                current_price=auction["current_price"],
                start_time=auction["start_time"].isoformat(),  # Convert datetime to string
                end_time=auction["end_time"].isoformat(),
                category=auction["category"]
            )
            for auction in closed_auctions
        ]
        return ActiveAuctionsResponse(auctions=auctions)
    
    def send_email(self, to_email, subject, message_body):
        # Email credentials
        sender_email = ADMIN_ADDRESS  # Replace with your email
        sender_password = EMAIL_APP_PASSWORD   # Replace with your email's app password

        # Email configuration
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = to_email
        message["Subject"] = subject
        message.attach(MIMEText(message_body, "plain"))

        try:
            # Connect to the Gmail SMTP server
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()  # Start TLS encryption
                server.login(sender_email, sender_password)  # Login
                server.send_message(message)  # Send email

            print(f"Email sent successfully to {to_email}")
            return True
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False
        

    def RespondToEmails(self, request, context):
        # Extract email ID and response text from the request
        email_id = request.email_id
        response_text = request.response_text

        # Fetch the email record from MongoDB
        email_record = self.dao.emails.find_one({"_id": email_id})

        if not email_record:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Email with ID {email_id} not found")
            return Response(message="Email not found")

        user_email = email_record.get("user_email")
        original_message = email_record.get("message")

        # Construct the email content
        email_subject = "Response to Your Query"
        email_body = (
            f"Dear User,\n\n"
            f"Thank you for your query:\n\n"
            f"\"{original_message}\"\n\n"
            f"Our response:\n\n"
            f"{response_text}\n\n"
            f"Best regards,\nSupport Team"
        )

        # Send the email (using a helper function)
        email_sent = self.send_email(user_email, email_subject, email_body)

        if not email_sent:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Failed to send the email")
            return Response(message="Failed to send email")

        # Update MongoDB to mark the email as responded
        self.dao.respond_to_email(email_id, response_text)

        return Response(message="Response sent successfully")
    
    def ViewUnrespondedEmails(self, request, context):
        # Fetch unresponded emails
        unresponded_emails = self.dao.get_unresponded_emails()

        # Convert MongoDB results to gRPC response
        emails = [
            Email(
                email_id=str(email["_id"]),
                user_email=email["user_email"],
                message=email["message"]
            )
            for email in unresponded_emails
        ]

        return UnrespondedEmailsResponse(emails=emails)



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    admin_service_pb2_grpc.add_AdminServiceServicer_to_server(AdminService(), server)
    server.add_insecure_port(f"[::]:{RPC_PORT}")
    print(f"Server started on port {RPC_PORT}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
