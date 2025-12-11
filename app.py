import streamlit as st
from datetime import date, timedelta, datetime
import pandas as pd
from streamlit_calendar import calendar
import holidays
import json

# ============= TRANSLATIONS =============
TRANSLATIONS = {
    'en': {
        'title': '🚂 PI Cadence Calculator - Agile Release Train',
        'config': '⚙️ Configuration',
        'year': 'Year',
        'num_pis': 'Number of PIs',
        'first_pi_date': 'First PI Start Date',
        'train_config': '🚂 Train Configuration',
        'train_name': 'Train Name',
        'train_color': 'Train Color',
        'offset': 'offset relative to',
        'days': 'days',
        'week': 'week',
        'before': 'before',
        'after': 'after',
        'same_day': 'same day',
        'hackathon': '🎯 Hackathon',
        'config_mode': 'Configuration mode',
        'auto_iteration': 'Automatic (by iteration)',
        'custom_dates': 'Custom dates',
        'iteration': 'Iteration',
        'week_in_iteration': 'Week within iteration',
        'start_hackathon': 'Hackathon Start',
        'end_hackathon': 'Hackathon End',
        'blocked_days': '🚫 Blocked Days',
        'include_canada_holidays': 'Include Canada statutory holidays',
        'custom_blocks': 'Custom blocked periods',
        'num_blocks': 'Number of periods',
        'period': 'Period',
        'start': 'Start',
        'end': 'End',
        'manual_holidays': '📅 Manual Holidays',
        'add_holiday': 'Add individual holidays',
        'num_holidays': 'Number of holidays',
        'holiday': 'Holiday',
        'holiday_name': 'Holiday name',
        'holiday_date': 'Date',
        'generate': '🔄 Generate Calendar',
        'edit_dates': '✏️ Edit Dates',
        'view_calendar': '👁️ View Calendar',
        'edit_mode_title': '✏️ Edit Event Dates',
        'edit_mode_info': 'Modify start and end dates of any event. Subsequent events will be automatically recalculated.',
        'both_trains': 'Both Trains',
        'calendar_view': '📅 Calendar View by Quarter',
        'show_in_calendar': 'Show in calendar:',
        'pi_planning': 'PI Planning',
        'event_details': '🔍 Event Details',
        'filter_train': 'Filter by Train',
        'filter_pi': 'Filter by PI',
        'filter_type': 'Filter by Type',
        'all': 'All',
        'iterations': 'Iterations',
        'duration': 'Duration',
        'summary_table': '📊 Summary Table',
        'event': 'Event',
        'download_csv': '📥 Download CSV',
        'configure_sidebar': '👈 Configure parameters in the sidebar and press "Generate Calendar"',
        'version': 'PI Cadence Calculator | Version 2.2',
        'saved': '✅ Saved',
        'language': 'Language',
        'save_config': '💾 Save/Load Configuration',
        'save_config_file': '📥 Download Configuration',
        'load_config_file': '📤 Upload Configuration',
        'config_saved': '✅ Configuration downloaded successfully!',
        'config_loaded': '✅ Configuration loaded successfully!',
        'config_error': '❌ Error loading configuration file'
    },
    'fr': {
        'title': '🚂 Calculateur de Cadence PI - Train de Livraison Agile',
        'config': '⚙️ Configuration',
        'year': 'Année',
        'num_pis': 'Nombre de PIs',
        'first_pi_date': 'Date de début du premier PI',
        'train_config': '🚂 Configuration des Trains',
        'train_name': 'Nom du Train',
        'train_color': 'Couleur du Train',
        'offset': 'décalage par rapport à',
        'days': 'jours',
        'week': 'semaine',
        'before': 'avant',
        'after': 'après',
        'same_day': 'même jour',
        'hackathon': '🎯 Hackathon',
        'config_mode': 'Mode de configuration',
        'auto_iteration': 'Automatique (par itération)',
        'custom_dates': 'Dates personnalisées',
        'iteration': 'Itération',
        'week_in_iteration': 'Semaine dans l\'itération',
        'start_hackathon': 'Début du Hackathon',
        'end_hackathon': 'Fin du Hackathon',
        'blocked_days': '🚫 Jours Bloqués',
        'include_canada_holidays': 'Inclure les jours fériés du Canada',
        'custom_blocks': 'Périodes bloquées personnalisées',
        'num_blocks': 'Nombre de périodes',
        'period': 'Période',
        'start': 'Début',
        'end': 'Fin',
        'manual_holidays': '📅 Jours Fériés Manuels',
        'add_holiday': 'Ajouter des jours fériés individuels',
        'num_holidays': 'Nombre de jours fériés',
        'holiday': 'Jour férié',
        'holiday_name': 'Nom du jour férié',
        'holiday_date': 'Date',
        'generate': '🔄 Générer le Calendrier',
        'edit_dates': '✏️ Modifier les Dates',
        'view_calendar': '👁️ Voir le Calendrier',
        'edit_mode_title': '✏️ Modifier les Dates d\'Événements',
        'edit_mode_info': 'Modifiez les dates de début et de fin de tout événement. Les événements suivants seront automatiquement recalculés.',
        'both_trains': 'Les Deux Trains',
        'calendar_view': '📅 Vue Calendrier par Trimestre',
        'show_in_calendar': 'Afficher dans le calendrier:',
        'pi_planning': 'Planification PI',
        'event_details': '🔍 Détails des Événements',
        'filter_train': 'Filtrer par Train',
        'filter_pi': 'Filtrer par PI',
        'filter_type': 'Filtrer par Type',
        'all': 'Tous',
        'iterations': 'Itérations',
        'duration': 'Durée',
        'summary_table': '📊 Tableau Récapitulatif',
        'event': 'Événement',
        'download_csv': '📥 Télécharger CSV',
        'configure_sidebar': '👈 Configurez les paramètres dans la barre latérale et appuyez sur "Générer le Calendrier"',
        'version': 'Calculateur de Cadence PI | Version 2.2',
        'saved': '✅ Enregistré',
        'language': 'Langue',
        'save_config': '💾 Sauvegarder/Charger Configuration',
        'save_config_file': '📥 Télécharger la Configuration',
        'load_config_file': '📤 Téléverser la Configuration',
        'config_saved': '✅ Configuration téléchargée avec succès!',
        'config_loaded': '✅ Configuration chargée avec succès!',
        'config_error': '❌ Erreur lors du chargement du fichier de configuration'
    }
}

st.set_page_config(page_title="PI Cadence Calculator", layout="wide")

# Language selector at the top
lang = st.sidebar.selectbox("🌐 Language / Langue", ["en", "fr"], format_func=lambda x: "English" if x == "en" else "Français")
t = TRANSLATIONS[lang]

st.title(t['title'])

# ============= CONFIGURATION SAVE/LOAD =============

def create_config_dict():
    """Create a dictionary with all current configuration"""
    config = {
        'version': '2.2',
        'language': lang,
        'year': st.session_state.get('config_year', 2026),
        'num_pis': st.session_state.get('config_num_pis', 4),
        'first_pi_date': st.session_state.get('config_first_pi_date', date(2026, 1, 6)).isoformat(),
        'train_a_name': st.session_state.get('config_train_a_name', 'Train A'),
        'train_a_color': st.session_state.get('config_train_a_color', '#3788d8'),
        'train_b_name': st.session_state.get('config_train_b_name', 'Train B'),
        'train_b_color': st.session_state.get('config_train_b_color', '#dc3545'),
        'train_b_offset': st.session_state.get('config_train_b_offset', 7),
        'hack_mode': st.session_state.get('config_hack_mode', 'auto'),
        'hack_iter': st.session_state.get('config_hack_iter', 3),
        'hack_week': st.session_state.get('config_hack_week', 1),
        'hack_start': st.session_state.get('config_hack_start', date(2026, 4, 15)).isoformat() if st.session_state.get('config_hack_mode') == 'custom' else None,
        'hack_end': st.session_state.get('config_hack_end', date(2026, 4, 19)).isoformat() if st.session_state.get('config_hack_mode') == 'custom' else None,
        'include_canada_holidays': st.session_state.get('config_include_canada', True),
        'custom_blocks': [
            {
                'start': block['start'].isoformat(),
                'end': block['end'].isoformat()
            } for block in st.session_state.get('config_custom_blocks', [])
        ],
        'manual_holidays': [
            {
                'name': holiday['name'],
                'date': holiday['date'].isoformat()
            } for holiday in st.session_state.get('config_manual_holidays', [])
        ]
    }
    return config

def load_config_from_dict(config):
    """Load configuration from dictionary into session state"""
    try:
        st.session_state['config_year'] = config.get('year', 2026)
        st.session_state['config_num_pis'] = config.get('num_pis', 4)
        st.session_state['config_first_pi_date'] = date.fromisoformat(config.get('first_pi_date', '2026-01-06'))
        st.session_state['config_train_a_name'] = config.get('train_a_name', 'Train A')
        st.session_state['config_train_a_color'] = config.get('train_a_color', '#3788d8')
        st.session_state['config_train_b_name'] = config.get('train_b_name', 'Train B')
        st.session_state['config_train_b_color'] = config.get('train_b_color', '#dc3545')
        st.session_state['config_train_b_offset'] = config.get('train_b_offset', 7)
        st.session_state['config_hack_mode'] = config.get('hack_mode', 'auto')
        st.session_state['config_hack_iter'] = config.get('hack_iter', 3)
        st.session_state['config_hack_week'] = config.get('hack_week', 1)
        
        if config.get('hack_start'):
            st.session_state['config_hack_start'] = date.fromisoformat(config['hack_start'])
        if config.get('hack_end'):
            st.session_state['config_hack_end'] = date.fromisoformat(config['hack_end'])
        
        st.session_state['config_include_canada'] = config.get('include_canada_holidays', True)
        
        # Load custom blocks
        custom_blocks = []
        for block in config.get('custom_blocks', []):
            custom_blocks.append({
                'start': date.fromisoformat(block['start']),
                'end': date.fromisoformat(block['end'])
            })
        st.session_state['config_custom_blocks'] = custom_blocks
        
        # Load manual holidays
        manual_holidays = []
        for holiday in config.get('manual_holidays', []):
            manual_holidays.append({
                'name': holiday['name'],
                'date': date.fromisoformat(holiday['date'])
            })
        st.session_state['config_manual_holidays'] = manual_holidays
        
        return True
    except Exception as e:
        st.error(f"{t['config_error']}: {str(e)}")
        return False

# Save/Load Section
st.sidebar.markdown("---")
st.sidebar.subheader(t['save_config'])

# Upload configuration
uploaded_file = st.sidebar.file_uploader(t['load_config_file'], type=['json'], key='config_uploader')
if uploaded_file is not None:
    try:
        config_data = json.load(uploaded_file)
        if load_config_from_dict(config_data):
            st.sidebar.success(t['config_loaded'])
            st.rerun()
    except Exception as e:
        st.sidebar.error(f"{t['config_error']}: {str(e)}")

st.sidebar.markdown("---")

# ============= HELPER FUNCTIONS =============

def add_business_days(start_date, num_days, blocked_dates=[]):
    """Add business days to a date (excludes weekends and blocked dates)"""
    current = start_date
    days_added = 0
    
    while days_added < num_days:
        current += timedelta(days=1)
        if current.weekday() < 5 and current not in blocked_dates:
            days_added += 1
    
    return current

def get_next_tuesday(start_date):
    """Find the next Tuesday from a given date"""
    days_ahead = 1 - start_date.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return start_date + timedelta(days=days_ahead)

def get_blocked_dates(year, custom_blocks=[], manual_holidays=[], include_canada=True):
    """Get all blocked dates: Canada holidays + custom periods + manual holidays"""
    blocked = set()
    
    # Canada holidays
    if include_canada:
        ca_holidays = holidays.Canada(years=[year, year+1])
        blocked = set(ca_holidays.keys())
    
    # Custom blocked periods
    for block in custom_blocks:
        current = block['start']
        while current <= block['end']:
            blocked.add(current)
            current += timedelta(days=1)
    
    # Manual holidays
    for holiday in manual_holidays:
        blocked.add(holiday['date'])
    
    return blocked

def calculate_pi_events(pi_start_date, pi_number, train_name, offset_days=0, blocked_dates=[]):
    """Calculate all events for a PI (Planning + 6 iterations)"""
    events = []
    
    adjusted_start = pi_start_date + timedelta(days=offset_days)
    
    # PI Planning (Tuesday and Wednesday)
    pi_planning_start = get_next_tuesday(adjusted_start)
    pi_planning_end = pi_planning_start + timedelta(days=1)
    
    events.append({
        "PI": f"PI Q{pi_number}",
        "Tren": train_name,
        "Evento": "PI Planning",
        "Inicio": pi_planning_start,
        "Fin": pi_planning_end,
        "Tipo": "planning",
        "ID": f"Q{pi_number}_{train_name}_planning"
    })
    
    iteration_start = pi_planning_end + timedelta(days=1)
    
    # 6 iterations of 10 business days each
    for i in range(1, 7):
        iter_end = add_business_days(iteration_start, 9, blocked_dates)
        
        events.append({
            "PI": f"PI Q{pi_number}",
            "Tren": train_name,
            "Evento": f"{t['iteration']} {i}",
            "Inicio": iteration_start,
            "Fin": iter_end,
            "Tipo": "iteration",
            "ID": f"Q{pi_number}_{train_name}_iter{i}"
        })
        
        iteration_start = add_business_days(iter_end, 1, blocked_dates)
    
    return events

def add_hackathon_event(events_train_a, events_train_b, hackathon_iteration=3, hackathon_week=1, custom_dates=None, lang='en'):
    """Add hackathon event"""
    t = TRANSLATIONS[lang]
    
    if custom_dates:
        return {
            "PI": "Multiple",
            "Tren": t['both_trains'],
            "Evento": f"🎯 {t['hackathon'].replace('🎯 ', '')}",
            "Inicio": custom_dates['start'],
            "Fin": custom_dates['end'],
            "Tipo": "hackathon",
            "ID": "hackathon_custom"
        }
    
    target_iteration = f"{t['iteration']} {hackathon_iteration}"
    
    for event in events_train_a:
        if event["Evento"] == target_iteration:
            iter_start = event["Inicio"]
            
            if hackathon_week == 1:
                hack_start = iter_start
            else:
                hack_start = add_business_days(iter_start, 5)
            
            hack_end = add_business_days(hack_start, 4)
            
            return {
                "PI": event["PI"],
                "Tren": t['both_trains'],
                "Evento": f"🎯 {t['hackathon'].replace('🎯 ', '')}",
                "Inicio": hack_start,
                "Fin": hack_end,
                "Tipo": "hackathon",
                "ID": f"{event['PI']}_hackathon"
            }
    
    return None

def recalculate_events_from_edit(all_events, edited_event_id, new_start, new_end, blocked_dates=[]):
    """Recalculate subsequent events after editing one"""
    edited_index = None
    for i, event in enumerate(all_events):
        if event.get("ID") == edited_event_id:
            all_events[i]["Inicio"] = new_start
            all_events[i]["Fin"] = new_end
            edited_index = i
            break
    
    if edited_index is None:
        return all_events
    
    edited_event = all_events[edited_index]
    
    if edited_event["Tipo"] == "iteration":
        pi = edited_event["PI"]
        tren = edited_event["Tren"]
        next_start = add_business_days(new_end, 1, blocked_dates)
        
        for i in range(edited_index + 1, len(all_events)):
            if (all_events[i]["PI"] == pi and 
                all_events[i]["Tren"] == tren and 
                all_events[i]["Tipo"] == "iteration"):
                
                all_events[i]["Inicio"] = next_start
                all_events[i]["Fin"] = add_business_days(next_start, 9, blocked_dates)
                next_start = add_business_days(all_events[i]["Fin"], 1, blocked_dates)
    
    return all_events

# ============= USER INTERFACE =============

st.sidebar.header(t['config'])

# Basic inputs
col1, col2 = st.sidebar.columns(2)
with col1:
    year = st.number_input(t['year'], min_value=2025, max_value=2030, 
                          value=st.session_state.get('config_year', 2026),
                          key='input_year')
    st.session_state['config_year'] = year
with col2:
    num_pis = st.number_input(t['num_pis'], min_value=1, max_value=4, 
                             value=st.session_state.get('config_num_pis', 4),
                             key='input_num_pis')
    st.session_state['config_num_pis'] = num_pis

first_pi_date = st.sidebar.date_input(
    t['first_pi_date'],
    value=st.session_state.get('config_first_pi_date', date(year, 1, 6)),
    key='input_first_pi_date'
)
st.session_state['config_first_pi_date'] = first_pi_date

st.sidebar.markdown("---")

# Train Configuration
st.sidebar.subheader(t['train_config'])

train_a_name = st.sidebar.text_input(f"{t['train_name']} A", 
                                     value=st.session_state.get('config_train_a_name', 'Train A'),
                                     key='input_train_a_name')
st.session_state['config_train_a_name'] = train_a_name

train_a_color = st.sidebar.color_picker(f"{t['train_color']} A", 
                                       value=st.session_state.get('config_train_a_color', '#3788d8'),
                                       key='input_train_a_color')
st.session_state['config_train_a_color'] = train_a_color

train_b_name = st.sidebar.text_input(f"{t['train_name']} B", 
                                     value=st.session_state.get('config_train_b_name', 'Train B'),
                                     key='input_train_b_name')
st.session_state['config_train_b_name'] = train_b_name

train_b_color = st.sidebar.color_picker(f"{t['train_color']} B", 
                                       value=st.session_state.get('config_train_b_color', '#dc3545'),
                                       key='input_train_b_color')
st.session_state['config_train_b_color'] = train_b_color

offset_index = {-7: 0, 0: 1, 7: 2}.get(st.session_state.get('config_train_b_offset', 7), 2)
train_b_offset = st.sidebar.radio(
    f"{train_b_name} {t['offset']} {train_a_name}:",
    options=[-7, 0, 7],
    format_func=lambda x: f"{x:+d} {t['days']} ({abs(x)//7} {t['week']} {t['before'] if x < 0 else t['after'] if x > 0 else t['same_day']})",
    index=offset_index,
    key='input_train_b_offset'
)
st.session_state['config_train_b_offset'] = train_b_offset

st.sidebar.markdown("---")

# Hackathon Configuration
st.sidebar.subheader(t['hackathon'])

hack_mode_index = 0 if st.session_state.get('config_hack_mode', 'auto') == 'auto' else 1
hack_mode = st.sidebar.radio(
    t['config_mode'],
    [t['auto_iteration'], t['custom_dates']],
    index=hack_mode_index,
    key='input_hack_mode'
)
st.session_state['config_hack_mode'] = 'auto' if hack_mode == t['auto_iteration'] else 'custom'

if hack_mode == t['auto_iteration']:
    hack_iter = st.sidebar.selectbox(f"{t['iteration']} ({t['hackathon'].replace('🎯 ', '')})", 
                                     [1,2,3,4,5,6], 
                                     index=st.session_state.get('config_hack_iter', 3) - 1,
                                     key='input_hack_iter')
    st.session_state['config_hack_iter'] = hack_iter
    
    hack_week = st.sidebar.radio(t['week_in_iteration'], [1, 2], 
                                 index=st.session_state.get('config_hack_week', 1) - 1,
                                 key='input_hack_week')
    st.session_state['config_hack_week'] = hack_week
    custom_hack_dates = None
else:
    col_h1, col_h2 = st.sidebar.columns(2)
    with col_h1:
        hack_start = st.sidebar.date_input(t['start_hackathon'], 
                                          value=st.session_state.get('config_hack_start', date(year, 4, 15)),
                                          key='input_hack_start')
        st.session_state['config_hack_start'] = hack_start
    with col_h2:
        hack_end = st.sidebar.date_input(t['end_hackathon'], 
                                        value=st.session_state.get('config_hack_end', date(year, 4, 19)),
                                        key='input_hack_end')
        st.session_state['config_hack_end'] = hack_end
    custom_hack_dates = {'start': hack_start, 'end': hack_end}
    hack_iter = 3
    hack_week = 1

st.sidebar.markdown("---")

# Blocked days configuration
st.sidebar.subheader(t['blocked_days'])

include_canada_holidays = st.sidebar.checkbox(t['include_canada_holidays'], 
                                              value=st.session_state.get('config_include_canada', True),
                                              key='input_include_canada')
st.session_state['config_include_canada'] = include_canada_holidays

# Custom blocked periods
st.sidebar.write(f"**{t['custom_blocks']}:**")
num_blocks = st.sidebar.number_input(t['num_blocks'], min_value=0, max_value=5, 
                                     value=len(st.session_state.get('config_custom_blocks', [{'start': date(year, 12, 15), 'end': date(year+1, 1, 3)}])),
                                     key='input_num_blocks')

custom_blocks = []
for i in range(num_blocks):
    st.sidebar.write(f"{t['period']} {i+1}")
    col_b1, col_b2 = st.sidebar.columns(2)
    
    default_blocks = st.session_state.get('config_custom_blocks', [])
    default_start = default_blocks[i]['start'] if i < len(default_blocks) else date(year, 12, 15)
    default_end = default_blocks[i]['end'] if i < len(default_blocks) else date(year+1, 1, 3)
    
    with col_b1:
        block_start = st.sidebar.date_input(t['start'], value=default_start, key=f"block_start_{i}")
    with col_b2:
        block_end = st.sidebar.date_input(t['end'], value=default_end, key=f"block_end_{i}")
    custom_blocks.append({'start': block_start, 'end': block_end})

st.session_state['config_custom_blocks'] = custom_blocks

st.sidebar.markdown("---")

# Manual holidays
st.sidebar.subheader(t['manual_holidays'])
st.sidebar.write(f"**{t['add_holiday']}:**")
num_manual_holidays = st.sidebar.number_input(t['num_holidays'], min_value=0, max_value=10, 
                                              value=len(st.session_state.get('config_manual_holidays', [])),
                                              key='input_num_holidays')

manual_holidays = []
for i in range(num_manual_holidays):
    st.sidebar.write(f"{t['holiday']} {i+1}")
    col_h1, col_h2 = st.sidebar.columns(2)
    
    default_holidays = st.session_state.get('config_manual_holidays', [])
    default_name = default_holidays[i]['name'] if i < len(default_holidays) else f"Holiday {i+1}"
    default_date = default_holidays[i]['date'] if i < len(default_holidays) else date(year, 1, 1)
    
    with col_h1:
        holiday_name = st.sidebar.text_input(t['holiday_name'], value=default_name, key=f"holiday_name_{i}")
    with col_h2:
        holiday_date = st.sidebar.date_input(t['holiday_date'], value=default_date, key=f"holiday_date_{i}")
    manual_holidays.append({'name': holiday_name, 'date': holiday_date})

st.session_state['config_manual_holidays'] = manual_holidays

# Download configuration button
config_json = json.dumps(create_config_dict(), indent=2)
st.sidebar.download_button(
    label=t['save_config_file'],
    data=config_json,
    file_name=f"pi_cadence_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
    mime="application/json",
    key='download_config'
)

# ============= EVENT CALCULATION =============

if st.sidebar.button(t['generate'], type="primary"):
    # Calculate blocked dates
    blocked_dates = get_blocked_dates(year, custom_blocks, manual_holidays, include_canada_holidays)
    
    all_events = []
    
    # Calculate for each PI
    current_pi_date = first_pi_date
    
    for pi_num in range(1, num_pis + 1):
        # Train A events
        events_a = calculate_pi_events(current_pi_date, pi_num, train_a_name, 0, blocked_dates)
        all_events.extend(events_a)
        
        # Train B events
        events_b = calculate_pi_events(current_pi_date, pi_num, train_b_name, train_b_offset, blocked_dates)
        all_events.extend(events_b)
        
        # Add Hackathon
        if hack_mode == t['auto_iteration']:
            hackathon = add_hackathon_event(events_a, events_b, hack_iter, hack_week, lang=lang)
        else:
            hackathon = add_hackathon_event(events_a, events_b, custom_dates=custom_hack_dates, lang=lang)
        
        if hackathon and pi_num == 1:
            all_events.append(hackathon)
        
        # Next PI: approximately 12 weeks later
        current_pi_date = add_business_days(current_pi_date, 60, blocked_dates)
    
    # Save to session state
    st.session_state['events'] = all_events
    st.session_state['blocked_dates'] = blocked_dates
    st.session_state['train_a_name'] = train_a_name
    st.session_state['train_b_name'] = train_b_name
    st.session_state['train_a_color'] = train_a_color
    st.session_state['train_b_color'] = train_b_color
    st.session_state['generated'] = True
    st.session_state['edit_mode'] = False
    st.session_state['lang'] = lang

# ============= VISUALIZATION =============

if st.session_state.get('generated', False):
    events = st.session_state['events']
    blocked_dates = st.session_state.get('blocked_dates', set())
    train_a_name = st.session_state.get('train_a_name', 'Train A')
    train_b_name = st.session_state.get('train_b_name', 'Train B')
    train_a_color = st.session_state.get('train_a_color', '#3788d8')
    train_b_color = st.session_state.get('train_b_color', '#dc3545')
    stored_lang = st.session_state.get('lang', 'en')
    t_display = TRANSLATIONS[stored_lang]
    
    # Button to toggle edit mode
    col_btn1, col_btn2 = st.columns([1, 5])
    with col_btn1:
        if st.button(t[('edit_dates' if not st.session_state.get('edit_mode', False) else 'view_calendar')]):
            st.session_state['edit_mode'] = not st.session_state.get('edit_mode', False)
            st.rerun()
    
    # ============= EDIT MODE =============
    if st.session_state.get('edit_mode', False):
        st.markdown(f"### {t['edit_mode_title']}")
        st.info(t['edit_mode_info'])
        
        # Group by PI and Train
        pis = sorted(list(set([e["PI"] for e in events if e["Tipo"] != "hackathon"])))
        
        for pi in pis:
            st.markdown(f"#### {pi}")
            
            trenes = sorted(list(set([e["Tren"] for e in events if e["PI"] == pi and e["Tren"] != t_display['both_trains']])))
            
            for tren in trenes:
                with st.expander(f"📋 {tren}", expanded=False):
                    pi_events = [e for e in events if e["PI"] == pi and e["Tren"] == tren]
                    
                    for event in pi_events:
                        col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                        
                        with col1:
                            st.write(f"**{event['Evento']}**")
                        
                        with col2:
                            new_start = st.date_input(
                                t['start'],
                                value=event["Inicio"],
                                key=f"start_{event['ID']}"
                            )
                        
                        with col3:
                            new_end = st.date_input(
                                t['end'],
                                value=event["Fin"],
                                key=f"end_{event['ID']}"
                            )
                        
                        with col4:
                            if st.button("💾", key=f"save_{event['ID']}"):
                                st.session_state['events'] = recalculate_events_from_edit(
                                    st.session_state['events'],
                                    event['ID'],
                                    new_start,
                                    new_end,
                                    blocked_dates
                                )
                                st.success(t['saved'])
                                st.rerun()
        
        # Edit Hackathon
        st.markdown(f"#### {t['hackathon']}")
        hack_events = [e for e in events if e["Tipo"] == "hackathon"]
        
        if hack_events:
            for event in hack_events:
                col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                
                with col1:
                    st.write(f"**{event['Evento']}**")
                
                with col2:
                    new_start = st.date_input(
                        t['start'],
                        value=event["Inicio"],
                        key=f"start_{event['ID']}"
                    )
                
                with col3:
                    new_end = st.date_input(
                        t['end'],
                        value=event["Fin"],
                        key=f"end_{event['ID']}"
                    )
                
                with col4:
                    if st.button("💾", key=f"save_{event['ID']}"):
                        for i, e in enumerate(st.session_state['events']):
                            if e.get("ID") == event['ID']:
                                st.session_state['events'][i]["Inicio"] = new_start
                                st.session_state['events'][i]["Fin"] = new_end
                        st.success(t['saved'])
                        st.rerun()
    
    # ============= CALENDAR VIEW =============
    else:
        st.markdown(f"### {t['calendar_view']}")
        
        # Train filter for calendar
        col_filter1, col_filter2 = st.columns([1, 4])
        with col_filter1:
            calendar_train_filter = st.selectbox(
                f"{t['show_in_calendar']}",
                [t['both_trains'], train_a_name, train_b_name]
            )
        
        # Convert events to FullCalendar format
        calendar_events = []
        
        for e in events:
            # Apply train filter
            if calendar_train_filter != t['both_trains']:
                if e["Tren"] not in [calendar_train_filter, t_display['both_trains']]:
                    continue
            
            # Determine color
            if e["Tipo"] == "hackathon":
                event_color = "#fd7e14"  # Orange
            elif e["Tipo"] == "planning":
                event_color = "#6c757d"  # Gray
            else:  # iteration
                event_color = train_a_color if e["Tren"] == train_a_name else train_b_color
            
            calendar_events.append({
                "title": f"{e['Tren']} - {e['Evento']}",
                "start": e["Inicio"].strftime("%Y-%m-%d"),
                "end": (e["Fin"] + timedelta(days=1)).strftime("%Y-%m-%d"),
                "color": event_color,
                "resourceId": e["Tren"]
            })
        
        # Calendar options
        calendar_options = {
            "editable": False,
            "selectable": False,
            "headerToolbar": {
                "left": "prev,next today",
                "center": "title",
                "right": "dayGridMonth,dayGridWeek,listYear"
            },
            "initialView": "dayGridMonth",
            "initialDate": str(events[0]["Inicio"]) if events else str(date.today()),
            "navLinks": True,
            "dayMaxEvents": True,
        }
        
        # Color legend
        col_legend1, col_legend2, col_legend3, col_legend4 = st.columns(4)
        with col_legend1:
            st.markdown(f'<div style="background-color:{train_a_color}; padding:10px; border-radius:5px; text-align:center; color:white;"><b>{train_a_name}</b></div>', unsafe_allow_html=True)
        with col_legend2:
            st.markdown(f'<div style="background-color:{train_b_color}; padding:10px; border-radius:5px; text-align:center; color:white;"><b>{train_b_name}</b></div>', unsafe_allow_html=True)
        with col_legend3:
            st.markdown(f'<div style="background-color:#6c757d; padding:10px; border-radius:5px; text-align:center; color:white;"><b>{t["pi_planning"]}</b></div>', unsafe_allow_html=True)
        with col_legend4:
            st.markdown(f'<div style="background-color:#fd7e14; padding:10px; border-radius:5px; text-align:center; color:white;"><b>{t["hackathon"].replace("🎯 ", "")}</b></div>', unsafe_allow_html=True)
        
        # Display calendar
        cal = calendar(events=calendar_events, options=calendar_options, key="pi_calendar")
        
        st.markdown("---")
        
        # ============= FILTERS AND DETAILS =============
        st.markdown(f"### {t['event_details']}")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_train = st.selectbox(t['filter_train'], [t['all'], train_a_name, train_b_name, t_display['both_trains']])
        with col2:
            filter_pi = st.selectbox(t['filter_pi'], [t['all']] + sorted(list(set([e["PI"] for e in events]))))
        with col3:
            filter_event = st.selectbox(t['filter_type'], [t['all'], t['pi_planning'], t['iterations'], t['hackathon'].replace('🎯 ', '')])
        
        # Apply filters
        filtered_events = events.copy()
        
        if filter_train != t['all']:
            filtered_events = [e for e in filtered_events if e["Tren"] == filter_train or e["Tren"] == t_display['both_trains']]
        
        if filter_pi != t['all']:
            filtered_events = [e for e in filtered_events if e["PI"] == filter_pi]
        
        if filter_event != t['all']:
            if filter_event == t['pi_planning']:
                filtered_events = [e for e in filtered_events if e["Tipo"] == "planning"]
            elif filter_event == t['iterations']:
                filtered_events = [e for e in filtered_events if e["Tipo"] == "iteration"]
            elif filter_event == t['hackathon'].replace('🎯 ', ''):
                filtered_events = [e for e in filtered_events if e["Tipo"] == "hackathon"]
        
        # Display as cards
        for e in sorted(filtered_events, key=lambda x: x["Inicio"]):
            color_map_emoji = {
                "planning": "🔵",
                "iteration": "🟢",
                "hackathon": "🟠"
            }
            
            with st.container(border=True):
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.subheader(f'{color_map_emoji.get(e["Tipo"], "⚪")} {e["Evento"]}')
                    st.caption(f'{e["PI"]} – {e["Tren"]}')
                with col_b:
                    days = (e["Fin"] - e["Inicio"]).days + 1
                    st.metric(t['duration'], f"{days} {t['days']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f'📍 **{t["start"]}:** {e["Inicio"].strftime("%d/%m/%Y (%A)")}')
                with col2:
                    st.write(f'🏁 **{t["end"]}:** {e["Fin"].strftime("%d/%m/%Y (%A)")}')
        
        # Summary table
        st.markdown("---")
        st.markdown(f"### {t['summary_table']}")
        
        df = pd.DataFrame(filtered_events)
        df[t['start']] = df['Inicio'].apply(lambda x: x.strftime('%d/%m/%Y'))
        df[t['end']] = df['Fin'].apply(lambda x: x.strftime('%d/%m/%Y'))
        df = df[['PI', 'Tren', 'Evento', t['start'], t['end']]]
        df.columns = ['PI', t['filter_train'].replace('Filter by ', '').replace('Filtrer par ', ''), t['event'], t['start'], t['end']]
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Download button
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=t['download_csv'],
            data=csv,
            file_name=f"pi_cadence_{year}.csv",
            mime="text/csv"
        )

else:
    st.info(t['configure_sidebar'])

st.markdown("---")
st.caption(t['version'])
