type ThemeModeType = {
  isDark: boolean;
}

class ThemeMode implements ThemeModeType {
  isDark = $state(false);
}

const themeMode = new ThemeMode();
export default themeMode;