# ComuniCook

ComuniCook is a test Python Arcade game exploring AI agents.

## How it Works

The game simulates a community around a local food distribution center. Initially, there are only a few people in the community. The community has a happiness level, which is inversely proportional to the average hunger of all members.

### Hunger and Happiness

Each person has a hunger level between 0-100. As time passes, hunger increases. If someone's hunger reaches 100, they will leave the community. Happiness is tied to the community's average hunger level: the hungrier the people, the less happy the community is.

### Community Growth

A happier community is more likely to attract new people, while a low happiness level decreases the likelihood of new members joining.

### Player Actions

The player can pick up food, cook it, and serve it to the hungriest person in the community. When someone eats, their hunger level resets to 0.

## Future Implementations

There is currently a money attribute, but it doesn't affect gameplay yet. The idea is to treat money as "donations," where a larger community generates more income. This money can be used to buy new equipment, like ovens or different types of food, allowing for faster and better food preparation.