#!/usr/bin/env python

import operator
import pprint

import click


platinum2copper = 1000
gold2copper = 100
electrum2copper = 50
silver2copper = 10


class Valuable(object):

    def __init__(self, name, short, value_in_cp):
        self.name = str(name)
        self.short = str(short)
        self.value_in_cp = int(value_in_cp)

    def __repr__(self):
        return "Valuable(name='{}', value_in_cp='{}')".format(
            self.name,
            self.value_in_cp,
        )

    def __str__(self):
        return "{}".format(
            self.name,
            # self.value_in_cp,
        )

    def __cmp__(self, other):
        return cmp(self.value_in_cp, other.value_in_cp)

    def __hash__(self):
        return hash((self.name, self.value_in_cp))


class Character(object):

    def __init__(self, name):
        self.name = name
        self.valuables = {}

    def add_valuable(self, valuable, num):
        if valuable not in self.valuables:
            self.valuables[valuable] = 0
        self.valuables[valuable] += num

    @property
    def total_value_in_copper(self):
        total = 0

        for valuable, num in self.valuables.iteritems():
            total += valuable.value_in_cp * num

        return total

    def __repr__(self):
        return "Character(name='{}', total_value_in_copper='{}')".format(
            self.name,
            self.total_value_in_copper,
        )

    def __str__(self):
        return "Character {} gets {} gp in valuables:\n{}".format(
            self.name,
            self.total_value_in_copper / gold2copper,
            pprint.pformat(self.valuables),
        )

    def __cmp__(self, other):
        return cmp(self.total_value_in_copper, other.total_value_in_copper)


def split(party, valuable, num_valuables):
    num_party = len(party)

    while num_valuables > 0:
        # if everybody is equal, split as many coins as possible
        if num_valuables >= num_party and party_equal(party):
            pre_split_valuables = num_valuables
            split_valuables, num_valuables = divmod(num_valuables, num_party)
            click.echo(
                "split {} {} into {} piles of {} with {} leftover...".format(
                    pre_split_valuables,
                    valuable,
                    num_party,
                    split_valuables,
                    num_valuables,
                )
            )
            for p in party:
                p.add_valuable(valuable=valuable, num=split_valuables)

        if num_valuables:
            click.echo("giving 1 of {} {} to the poorest character...".format(
                num_valuables,
                valuable,
            ))

            # pick the poorest party member
            p = min(party)

            p.add_valuable(valuable=valuable, num=1)
            num_valuables -= 1


def party_equal(party):
    if len(party) <= 1:
        return True

    p0_value = party[0].total_value_in_copper

    for p in party[1:]:
        if p.total_value_in_copper != p0_value:
            return False

    return True


@click.command()
@click.option('--cp', '--copper', prompt=True, type=int)
@click.option('--sp', '--silver', prompt=True, type=int)
@click.option('--ep', '--electrum', prompt=True, type=int)
@click.option('--gp', '--gold', prompt=True, type=int)
@click.option('--pp', '--platinum', prompt=True, type=int)
@click.option('-n', '--num-party', prompt=True, type=int)
def main(
    copper,
    electrum,
    gold,
    num_party,
    platinum,
    silver,
):
    valuables = {}

    party = []
    for x in xrange(num_party):
        party.append(Character(x))

    if platinum:
        valuables[Valuable('platinum', 'pp', 1000)] = platinum
    if gold:
        valuables[Valuable('gold', 'gp', 100)] = gold
    if electrum:
        valuables[Valuable('electrum', 'ep', 50)] = electrum
    if silver:
        valuables[Valuable('silver', 'sp', 10)] = silver
    if copper:
        valuables[Valuable('copper', 'cp', 1)] = copper

    for valuable, num in sorted(
        valuables.items(),
        key=operator.itemgetter(0),  # sort by key which sorts by the value in copper
        reverse=True
    ):
        split(party, valuable, num)

    click.echo("")
    if party_equal(party):
        click.echo("The loot divided equally :)")
    else:
        click.echo("The loot did not divide equally :(")

    map(click.echo, party)


if __name__ == '__main__':
    main()
