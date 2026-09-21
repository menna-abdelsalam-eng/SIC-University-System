#Program's entry point
from registration_system import RegistrationSystem
from Uni_Main_Menu import Main_Menu
from JSONDataManager import JSONDataManager

if __name__ == "__main__":
    #initializing system and loading pre-saved data
    system = RegistrationSystem()

    data_manager = JSONDataManager()
    data_manager.load_data(system)

    main_menu = Main_Menu(system)
    main_menu.run_menu()

    data_manager.save_data(system)

