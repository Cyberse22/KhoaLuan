import { NavigationContainer } from '@react-navigation/native';
import React from 'react';
import DrawerNavigator from './components/Home/DrawerNavigator';

const App = () => {
  return (
    <NavigationContainer>
      <DrawerNavigator />
    </NavigationContainer>
  )
}

export default App;