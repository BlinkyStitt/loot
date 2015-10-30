#!/usr/bin/env python

import pprint

import click


platinum2copper = 1000
gold2copper = 100
electrum2copper = 50
silver2copper = 10


class Character(object):

    def __init__(self, name, cp=0, ep=0, sp=0, gp=0, pp=0):
        self.name = name
        self.cp = cp
        self.ep = ep
        self.sp = sp
        self.gp = gp
        self.pp = pp

    def add_coin(self, coin_type, num):
        current_coins = getattr(self, coin_type)
        setattr(self, coin_type, current_coins + num)

    @property
    def total_copper(self):
        return (
            self.pp * platinum2copper +
            self.gp * gold2copper +
            self.sp * silver2copper +
            self.ep * electrum2copper +
            self.cp
        )

    def __repr__(self):
        return "Character(name='{}', total_copper='{}')".format(
            self.name,
            self.total_copper,
        )

    def __str__(self):
        return "Character {}: {}".format(
            self.name,
            pprint.pformat({
                'pp': self.pp,
                'gp': self.gp,
                'sp': self.sp,
                'ep': self.ep,
                'cp': self.cp,
            }),
        )

    def __cmp__(self, other):
        return cmp(self.total_copper, other.total_copper)


def split(party, num_coins, coin_type):
    num_party = len(party)

    while num_coins > 0:
        # if everybody is equal, split as many coins as possible
        if num_coins >= num_party and party_equal(party):
            pre_split_coins = num_coins
            split_coins, num_coins = divmod(num_coins, num_party)
            click.echo("split {} {} into {} piles of {} with {} leftover...".format(
                pre_split_coins,
                coin_type,
                num_party,
                split_coins,
                num_coins,
            ))
            for p in party:
                p.add_coin(coin_type, split_coins)

        if num_coins:
            click.echo("dividing {} {}...".format(num_coins, coin_type))

            # pick the party member with the least amount of total_copper
            p = min(party)

            # setattr(p, coin_type, getattr(p, coin_type) + 1)
            p.add_coin(coin_type, 1)
            num_coins -= 1


def party_equal(party):
    if len(party) <= 1:
        return True

    p0_total_copper = party[0].total_copper

    for p in party[1:]:
        if p.total_copper != p0_total_copper:
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
    party = []
    for x in xrange(num_party):
        party.append(Character(x))

    split(party, platinum, 'pp')
    split(party, gold, 'gp')
    split(party, silver, 'sp')
    split(party, electrum, 'ep')
    split(party, copper, 'cp')

    click.echo("")
    if party_equal(party):
        click.echo("The loot divided equally :)")
    else:
        click.echo("The loot did not divide equally :(")

    map(click.echo, party)


if __name__ == '__main__':
    main()
