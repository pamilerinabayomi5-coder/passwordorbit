from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("🔑 Generate Password", callback_data="menu_generate")],
        [InlineKeyboardButton("⚙️ Settings", callback_data="menu_settings")],
        [InlineKeyboardButton("ℹ️ Help", callback_data="menu_help"),
         InlineKeyboardButton("🚀 About", callback_data="menu_about")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_settings_keyboard(prefs: dict) -> InlineKeyboardMarkup:
    def check(val): return "✅" if val else "❌"
    
    keyboard = [
        [InlineKeyboardButton(f"Length: {prefs['length']}", callback_data="set_len_prompt"),
         InlineKeyboardButton(f"Count: {prefs['quantity']}", callback_data="set_qty_prompt")],
        [InlineKeyboardButton(f"Uppercase {check(prefs['uppercase'])}", callback_data="toggle_uppercase"),
         InlineKeyboardButton(f"Lowercase {check(prefs['lowercase'])}", callback_data="toggle_lowercase")],
        [InlineKeyboardButton(f"Numbers {check(prefs['numbers'])}", callback_data="toggle_numbers"),
         InlineKeyboardButton(f"Symbols {check(prefs['symbols'])}", callback_data="toggle_symbols")],
        [InlineKeyboardButton(f"Exclude Ambiguous {check(prefs['exclude_ambiguous'])}", callback_data="toggle_exclude_ambiguous")],
        [InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="menu_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_generation_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("🔄 Generate Again", callback_data="action_generate_now")],
        [InlineKeyboardButton("💡 Copy Tips", callback_data="action_copy_tips")],
        [InlineKeyboardButton("⬅️ Main Menu", callback_data="menu_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_to_main_keyboard() -> InlineKeyboardMarkup:
    keyboard = [[InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="menu_main")]]
    return InlineKeyboardMarkup(keyboard)
