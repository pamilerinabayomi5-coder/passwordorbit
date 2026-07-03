import sys
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler
from config import BOT_TOKEN, logger
import database
import handlers

def main():
    """Application main runtime initialization entry point."""
    # Enforce SQLite storage check initialization routines
    database.init_db()
    
    # Instantiation of structural app context builder interfaces
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Conversation setup definitions mappings
    length_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(handlers.prompt_length_change, pattern="^set_len_prompt$")],
        states={handlers.EDIT_LENGTH: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.save_length_change)]},
        fallbacks=[CommandHandler("cancel", handlers.cancel_conversation)],
        per_chat=True
    )
    
    quantity_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(handlers.prompt_quantity_change, pattern="^set_qty_prompt$")],
        states={handlers.EDIT_QUANTITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.save_quantity_change)]},
        fallbacks=[CommandHandler("cancel", handlers.cancel_conversation)],
        per_chat=True
    )
    
    # Register structured workflow router components
    application.add_handler(CommandHandler("start", handlers.start_command))
    application.add_handler(length_conv)
    application.add_handler(quantity_conv)
    application.add_handler(CallbackQueryHandler(handlers.menu_button_handler, pattern="^menu_"))
    application.add_handler(CallbackQueryHandler(handlers.toggle_preference_handler, pattern="^toggle_"))
    application.add_handler(CallbackQueryHandler(handlers.action_button_handler, pattern="^action_"))
    
    # Exception boundary integration hook definitions
    application.add_error_handler(handlers.error_logging_handler)
    
    logger.info("PasswordOrbitBot initialization completed. Commencing continuous operation polling...")
    
    # Run loop processes orchestration
    application.run_polling()

if __name__ == "__main__":
    main()
