import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import * as React from 'react';
import { Text, View } from 'react-native';
import MyStyles from './styles/MyStyles';

function HomeScreen() {
  return(
    <View style={MyStyles.HomeScreen}>
      <Text>Home Screen</Text>
    </View>
  )
}

const Stack = createNativeStackNavigator();

function App(){
  return(
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name = "Home" component={HomeScreen}/>
      </Stack.Navigator>
    </NavigationContainer>
  )
}

export default App;