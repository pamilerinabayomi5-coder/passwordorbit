from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from config import logger
import database
import keyboards
import password_generator
import utils

# Define active sequential state allocations for structural changes
EDIT_LENGTH, EDIT_QUANTITY = range(2)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responds to /start endpoint."""
    user = update.effective_user
    database.add_user_if_not_exists(user.id, user.username, user.first_name)
    logger.info(f"User {user.id} initiated execution via /start.")
    
    welcome_text = (
        "Welcome to *PasswordOrbitBot*\\.\n"
        "I can generate highly secure passwords instantly using cryptographically strong generation principles\\.\n\n"
        "Choose an option below:"
    )
    
    if update.message:
        await update.message.reply_text(welcome_text, parse_mode="MarkdownV2", reply_markup=keyboards.get_main_menu_keyboard())
    else:
        await update.callback_query.message.edit_text(welcome_text, parse_mode="MarkdownV2", reply_markup=keyboards.get_main_menu_keyboard())

async def menu_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processes core main navigation inline queries."""
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = update.effective_user.id
    
    if data == "menu_main":
        await start_command(update, context)
        
    elif data == "menu_generate":
        await execute_generation_flow(query, user_id)
        
    elif data == "menu_settings":
        prefs = database.get_user_preferences(user_id)
        await query.edit_text(
            "⚙️ *PasswordOrbit Preferences*\nCustomize your generation specifications below\\. Changes save immediately\\.",
            parse_mode="MarkdownV2",
            reply_markup=keyboards.get_settings_keyboard(prefs)
        )
        
    elif data == "menu_help":
        help_text = (
            "💡 *How to Use PasswordOrbitBot*\n\n"
            "1️⃣ Set configuration parameters inside the *Settings* portal\\.\n"
            "2️⃣ Tap *Generate Password* to print immediate safe outputs\\.\n"
            "3️⃣ Double Click or long press on safe monospace blocks to instant copy\\.\n\n"
            "All generated instances are structured via Python's underlying system architecture engine `secrets` module for high entropy safety\\."
        )
        await query.edit_text(help_text, parse_mode="MarkdownV2", reply_markup=keyboards.get_back_to_main_keyboard())
        
    elif data == "menu_about":
        about_text = (
            "🚀 *About PasswordOrbitBot*\n"
            "• *Version:* 1\\.0\\.0\n"
            "• *Security:* Cryptographically sound system `secrets` module applied directly\\.\n"
            "• *Privacy:* Passwords are never stored on runtime logs or persistent database components\\.\n"
            "• *Developer:* Independent Creator Placeholder"
        )
        await query.edit_text(about_text, parse_mode="MarkdownV2", reply_markup=keyboards.get_back_to_main_keyboard())

async def toggle_preference_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles inverse state updates for config parameters."""
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    
    # Extract string flag
    pref_key = query.data.replace("toggle_", "")
    prefs = database.get_user_preferences(user_id)
    
    current_val = prefs.get(pref_key, 1)
    new_val = 0 if current_val == 1 else 1
    
    database.update_user_preference(user_id, pref_key, new_val)
    
    updated_prefs = database.get_user_preferences(user_id)
    await query.edit_reply_markup(reply_markup=keyboards.get_settings_keyboard(updated_prefs))

async def execute_generation_flow(query, user_id: int):
    """Core functional orchestrator for deploying structural output evaluations."""
    prefs = database.get_user_preferences(user_id)
    
    try:
        passwords = password_generator.generate_secure_passwords(
            length=prefs["length"],
            use_upper=bool(prefs["uppercase"]),
            use_lower=bool(prefs["lowercase"]),
            use_numbers=bool(prefs["numbers"]),
            use_symbols=bool(prefs["symbols"]),
            exclude_ambiguous=bool(prefs["exclude_ambiguous"]),
            quantity=prefs["quantity"]
        )
        
        response_lines = ["🔑 *Your Secure Output Generated:*", ""]
        for pwd in passwords:
            escaped_pwd = utils.escape_markdown_v2(pwd)
            response_lines.append(f"`{escaped_pwd}`")
            
        response_text = "\n".join(response_lines)
        await query.edit_text(response_text, parse_mode="MarkdownV2", reply_markup=keyboards.get_generation_keyboard())
        
    except ValueError as val_err:
        logger.warning(f"Validation failure logic met by user {user_id}: {val_err}")
        err_msg = utils.escape_markdown_v2(str(val_err))
        await query.edit_text(
            f"❌ *Configuration Constraint Issue:*\n{err_msg}\n\nPlease alter configuration selections within your Settings menu and try again\\.",
            parse_mode="MarkdownV2",
            reply_markup=keyboards.get_back_to_main_keyboard()
        )

async def action_button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processes runtime interactive requests post-generation."""
    query = update.callback_query
    await query.answer()
    user_id = update.effective_user.id
    
    if query.data == "action_generate_now":
        await execute_generation_flow(query, user_id)
    elif query.data == "action_copy_tips":
        tips = (
            "💡 *Telegram Desktop & Mobile Tips*:\n"
            "Tap or Long Press once directly on any of the monospace formatted strings inside the password block to instantly copy it to your system clipboard\\."
        )
        await query.edit_text(tips, parse_mode="MarkdownV2", reply_markup=keyboards.get_back_to_main_keyboard())

# Interactive state changes logic transitions via conversations
async def prompt_length_change(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_text("🔢 Please enter your desired length input \\(*Value between 4 and 128*\\):", parse_mode="MarkdownV2")
    return EDIT_LENGTH

async def save_length_change(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    user_id = update.effective_user.id
    
    if not text.isdigit() or not (4 <= int(text) <= 128):
        await update.message.reply_text("❌ Invalid input. Please enter an integer between 4 and 128.")
        return EDIT_LENGTH
        
    database.update_user_preference(user_id, "length", int(text))
    prefs = database.get_user_preferences(user_id)
    await update.message.reply_text(
        "✅ Configuration length updated successfully.",
        reply_markup=keyboards.get_settings_keyboard(prefs)
    )
    return ConversationHandler.END

async def prompt_quantity_change(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_text("🔢 Enter target password generation quantity count \\(*Value between 1 and 20*\\):", parse_mode="MarkdownV2")
    return EDIT_QUANTITY

async def save_quantity_change(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    user_id = update.effective_user.id
    
    if not text.isdigit() or not (1 <= int(text) <= 20):
        await update.message.reply_text("❌ Invalid input. Please enter an integer between 1 and 20.")
        return EDIT_QUANTITY
        
    database.update_user_preference(user_id, "quantity", int(text))
    prefs = database.get_user_preferences(user_id)
    await update.message.reply_text(
        "✅ Generation collection output quantity limit preference verified and saved.",
        reply_markup=keyboards.get_settings_keyboard(prefs)
    )
    return ConversationHandler.END

async def cancel_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Process tracking cancelled.", reply_markup=keyboards.get_main_menu_keyboard())
    return ConversationHandler.END

async def error_logging_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Central processing unit handling infrastructure exception metrics."""
    logger.error(f"Global Update error event tracking caught instance: {context.error}", exc_info=context.error)
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(
            "⚠️ An unexpected operational exception was caught on server communications. Please try again or re-verify details shortly."
        )
