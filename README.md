# ComuniCook

ComuniCook is a test Python Arcade game exploring AI agents.

## How it Works

The game simulates a community around a local food distribution center.
Initially, there are only a few people in the community. The community has a
happiness level, which is inversely proportional to the average hunger of all
members.

### Hunger and Happiness

Each person has a hunger level between 0-100. As time passes, hunger increases.
If someone's hunger reaches 100, they will leave the community. Happiness is
tied to the community's average hunger level: the hungrier the people, the less
happy the community is.

### Queue system

The restaurant has a queue. When you serve a food on the plates, the food will
go to the first person on the queue. A person joins a queue based on a chance
including the size of the queue and their hunger. The hungrier a person, the
more likely they will join the queue, big queue sizes lower the chance somewhat.

#### Swap places

When a new person joins the queue, someone in line may swap places with them if
the new person’s hunger is significantly greater. As the community grows, more
money flows into the restaurant, increasing the likelihood of serving more food.

### Share food

When the person in line finally get its food, they have a choice to potentially
share the food with someone hungrier in line. This in turn decreases the
nutrition that they get from the food but someone else gets a little less
hungry.

### Community Growth

A happier community is more likely to attract new people, while a low happiness
level decreases the likelihood of new members joining.

### Money

The restaurant has a money attribute. With money it is possible to buy new
equipment for the restaurant, such as ovens (and faster ovens!) and plate
tables. The larger the community the more money the restaurant receives.

### Player Actions

The player can pick up food, cook it, and serve to people in the queue. When
someone eats, their hunger decreases accordingly with the food nutrition.

Players can also open the buy menu (by pressing "M") and use saved money to
purchase new equipment.

### Assistants

Assistants can be hired to help you cook and server food for the community.

## Future Implementations

In future implementations there are plans to add new buying options, such as new
types of food.
